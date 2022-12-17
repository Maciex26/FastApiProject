from locust import HttpUser, task


class PerformanceTests(HttpUser):

    @task
    def prime(self):
        self.client.get(url='prime/500')

    @task
    def invert(self):
        in_file = open('pic.jpg', 'rb')
        data = in_file.read()
        self.client.post(url="picture/invert", files={'file': data})

    @task
    def read_current_user(self):
        self.client.get(url='time', auth=("test", "test"))
