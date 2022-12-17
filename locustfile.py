from locust import HttpUser, task


class PerformanceTests(HttpUser):

    @task
    def prime_number(self):
        self.client.get(url='prime/500')

    @task
    def post_img(self):
        in_file = open('pic.jpg', 'rb')
        data = in_file.read()
        self.client.post(url="picture/invert", files={'file': data})

    @task
    def check_user(self):
        self.client.get(url='time', auth=("test", "test"))
