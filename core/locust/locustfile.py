from locust import HttpUser, task, between


class QuickstartUser(HttpUser):
    def on_start(self):
        # getting & converting a response to JSON
        response = self.client.post(
            "/accounts/api/v1/jwt/create/",
            data={"email": "admin@admin.com", "password": "1101799"},
        ).json()
        self.client.headers = {
            "Authorization": f"Bearer {response.get('access', None)}"
        }

    @task
    def task_list(self):
        self.client.get("blog/api/v1/posts/")
