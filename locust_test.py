from locust import HttpUser, task, between



class StressTest(HttpUser):
    wait_time = between(1, 3)
   

    @task(1)
    def test_text_endpoint(self):
        payload = {}

        files=[
        ('image',('cat.jpg',open('cat.jpg','rb'),'image/jpeg'))
        ]
        
        url = "/clip?text=cat&text=girl%2Ca%20cat"
        res = self.client.post(
            url=url,
            headers={},
            data=payload,
            files=files
        )