from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from course.models import Course


class CourseAPITestCase(APITestCase):
    def setUp(self):
        self.course = Course.objects.create(
            title="Advanced Mathematics",
            course_code="math301",  # Stored in lowercase
            description="An advanced course"
        )
        self.list_url = reverse("course-list")
        self.detail_url = reverse("course-detail", kwargs={"pk": self.course.id})
        self.invalid_detail_url = reverse("course-detail", kwargs={"pk": 999})

    # --- Core CRUD Functionality ---

    def test_list_courses(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["course_code"], "MATH301")  # Assert uppercase

    def test_retrieve_course(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["course_code"], "MATH301")  # Assert uppercase

    def test_create_course(self):
        data = {
            "title": "Physics I",
            "course_code": "phy101",
            "description": "Introductory Physics course"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["course_code"], "PHY101")  # Output is uppercased

    def test_update_course(self):
        update_data = {
            "title": "Advanced Math II",
            "course_code": "math302",
            "description": "Updated"
        }
        response = self.client.put(self.detail_url, update_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["course_code"], "MATH302")

    def test_partial_update_course(self):
        patch_data = {"course_code": "math400"}
        response = self.client.patch(self.detail_url, patch_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["course_code"], "MATH400")

    def test_delete_course(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # --- Negative Cases ---

    def test_retrieve_nonexistent_course(self):
        response = self.client.get(self.invalid_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_course_missing_fields(self):
        data = {"title": "Invalid"}
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("course_code", response.data)

    def test_create_course_exceeding_max_lengths(self):
        data = {
            "title": "T" * 1001,
            "course_code": "C" * 11,
            "description": "D" * 10001
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_nonexistent_course(self):
        data = {
            "title": "Ghost",
            "course_code": "ghost101",
            "description": "Not real"
        }
        response = self.client.put(self.invalid_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_partial_update_invalid_data(self):
        response = self.client.patch(self.detail_url, {"course_code": "X" * 11})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_nonexistent_course(self):
        response = self.client.delete(self.invalid_detail_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # --- Edge Cases ---

    def test_course_code_stored_lowercase(self):
        response = self.client.post(self.list_url, {
            "title": "Case Normalization",
            "course_code": "MiXeDcAsE1",
            "description": "Check casing"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        course = Course.objects.get(id=response.data["id"])
        self.assertEqual(course.course_code, "mixedcase1")  # Stored in lowercase
        self.assertEqual(response.data["course_code"], "MIXEDCASE1")  # Returned in uppercase

    def test_course_code_uppercase_on_update(self):
        response = self.client.patch(self.detail_url, {"course_code": "UpDaTeD123"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.course.refresh_from_db()
        self.assertEqual(self.course.course_code, "updated123")
        self.assertEqual(response.data["course_code"], "UPDATED123")


    def test_course_code_displayed_uppercase_in_list(self):
        Course.objects.create(title="Another", course_code="lowercase", description="Test")
        response = self.client.get(self.list_url)
        course_codes = [course["course_code"] for course in response.data]
        for code in course_codes:
            self.assertTrue(code.isupper())

    def test_unicode_course_fields(self):
        data = {
            "title": "数学课程",
            "course_code": "uni101",
            "description": "学习 is fun 🚀"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["course_code"], "UNI101")

    def test_sql_injection_like_input(self):
        data = {
            "title": "Robert'); DROP TABLE Students;--",
            "course_code": "sql101",
            "description": "Testing input"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["course_code"], "SQL101")

from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .models import Course, CourseInstance

class CourseInstanceAPITestCase(APITestCase):
    def setUp(self):
        self.course1 = Course.objects.create(
            title="Math", course_code="MATH101", description="math desc"
        )
        self.course2 = Course.objects.create(
            title="Physics", course_code="PHY101", description="phy desc"
        )
        self.instance1 = CourseInstance.objects.create(
            year="2025", semester=1, course=self.course1
        )
        self.base_url = reverse("create-delete-instance")
        self.list_url = reverse(
            "view-instances-for-year-sem", kwargs={"year": 2025, "semester": 1}
        )
        self.detail_url = reverse(
            "view-instances-for-year-sem-courseId",
            kwargs={"year": 2025, "semester": 1, "courseId": self.course1.id},
        )
        self.invalid_year_sem_url = reverse(
            "view-instances-for-year-sem", kwargs={"year": 1900, "semester": 2}
        )
        self.invalid_detail_url = reverse(
            "view-instances-for-year-sem-courseId",
            kwargs={"year": 1900, "semester": 2, "courseId": 999},
        )

    # --- POST /instances/ ---

    def test_create_instance_success(self):
        data = {
            "course_id": str(self.course2.id),
            "year": 2025,
            "semester": 1,
        }
        resp = self.client.post(self.base_url, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data["course_code"], self.course2.course_code.upper())
        self.assertEqual(resp.data["course_id"], str(self.course2.id))
        self.assertTrue(CourseInstance.objects.filter(course=self.course2, year="2025", semester=1).exists())

    def test_create_instance_invalid_course(self):
        data = {"course_id": "9999", "year": 2025, "semester": 1}
        resp = self.client.post(self.base_url, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Course '9999' does not exist", str(resp.data))

    def test_create_duplicate_instance(self):
        data = {
            "course_id": str(self.course1.id),
            "year": 2025,
            "semester": 1,
        }
        resp = self.client.post(self.base_url, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("already exists", str(resp.data))

    # --- GET /instances/{year}/{semester}/ ---

    def test_list_instances_for_year_sem(self):
        resp = self.client.get(self.list_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertEqual(len(resp.data), 1)
        self.assertEqual(resp.data[0]["course_id"], str(self.course1.id))

    def test_list_instances_no_match(self):
        resp = self.client.get(self.invalid_year_sem_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # No instances: expect empty list
        self.assertEqual(resp.data, [])

    # --- DELETE /instances/{year}/{semester}/{courseId}/ ---

    def test_delete_instance_success(self):
        resp = self.client.delete(self.detail_url)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertTrue("deleted successfully" in resp.data.get("result", "").lower())
        self.assertFalse(CourseInstance.objects.filter(pk=self.instance1.pk).exists())

    def test_delete_instance_not_found(self):
        resp = self.client.delete(self.invalid_detail_url)
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("No Instance exists", resp.data.get("error", ""))

    def test_create_instance_missing_fields(self):
        data = {"course_id": str(self.course1.id)}  # Missing year and semester
        resp = self.client.post(self.base_url, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("year", resp.data)
        self.assertIn("semester", resp.data)

    def test_create_instance_invalid_year_format(self):
        data = {"course_id": str(self.course1.id), "year": "20a5", "semester": 1}
        resp = self.client.post(self.base_url, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_instance_leap_year(self):
        # Should be valid — edge year format check
        data = {"course_id": str(self.course1.id), "year": 2024, "semester": 2}
        resp = self.client.post(self.base_url, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_create_instance_uppercase_course_id(self):
        data = {"course_id": str(self.course1.id).upper(), "year": 2025, "semester": 2}
        resp = self.client.post(self.base_url, data, format="json")
        # should pass since IDs are numeric, but useful if UUIDs are used in future
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)

    def test_large_year_value(self):
        data = {"course_id": str(self.course1.id), "year": 9999, "semester": 1}
        resp = self.client.post(self.base_url, data, format="json")
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
