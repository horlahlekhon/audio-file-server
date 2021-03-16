import json
from pathlib import Path

from werkzeug.datastructures import FileStorage

from app.models.model import AudioBook
from tests.utils.base import BaseTestCase


class TestAudioAPI(BaseTestCase):

    def setUp(self):
        self.audio_file_path = Path("tests/utils/littleaudio.wav")
        self.invalid_file_path = Path("tests/utils/invalid.txt")
        self.valid_file = FileStorage(stream=open(self.audio_file_path, 'rb'), filename="audio_book",
                                      content_type="audio/wave")
        self.invalid_file = FileStorage(stream=open(self.invalid_file_path, 'rb'), filename="audio_book",
                                        content_type="text/plain")
        super(TestAudioAPI, self).setUp()

    def tearDown(self):
        self.valid_file = None
        self.invalid_file = None
        super(TestAudioAPI, self).tearDown()

    def test_create_audio_data(self):
        req_data = {
            "filetype": "audio_book",
            "title": "hight",
            "author": "dan",
            "narrator": "narrator",
            "duration": 123456
        }
        response = self.client.post("/api/audio/create", data=json.dumps(req_data),
                                    content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEquals(data["audiobook"]["uploaded_time"], None)
        self.assertEquals(data["audiobook"]["title"], req_data["title"])
        self.assertEquals(response.status_code, 200)
        self.assertIsNone(data["audiobook"]["uploaded_time"])

    def test_reject_create_with_bad_data(self):
        req_data = {
            "filetype": "audio_bookf",
            "title": "hight",
            "author": "dan",
            "narrator": "narrator",
            "duration": 123456
        }
        response = self.client.post("/api/audio/create", data=json.dumps(req_data),
                                    content_type="application/json")
        data = json.loads(response.data.decode())
        self.assertEquals(data["status"], False)
        self.assertEquals(response.status_code, 400)

    def test_get_audio_data(self):
        req_data = {
            "title": "hight",
            "author": "dan",
            "narrator": "narrator",
            "duration": 123456
        }
        s = AudioBook(**req_data)
        self.db.session.add(s)
        self.db.session.commit()
        resp = self.client.get(f"/api/audio/audio_book/{s.id}", content_type="application/json")
        data = json.loads(resp.data.decode())
        self.assertEquals(resp.status_code, 200)
        self.assertEquals(data["audiobook"]["duration"], req_data["duration"])

    def test_return_404_on_get_audio_that_doesnt_exist(self):
        resp = self.client.get(f"/api/audio/audio_book/30", content_type="application/json")
        data = json.loads(resp.data.decode())
        self.assertEquals(resp.status_code, 404)

    def test_delete_successfully_remove_audio_from_db(self):
        req_data = {
            "title": "hight",
            "author": "dan",
            "narrator": "narrator",
            "duration": 123456
        }
        s = AudioBook(**req_data)
        self.db.session.add(s)
        self.db.session.commit()
        resp = self.client.delete(f"/api/audio/audio_book/{s.id}", content_type="application/json")
        data = AudioBook.query.get(s.id)
        self.assertEquals(data, None)
        self.assertEquals(resp.status_code, 200)

    def test_update_to_upload_audio_file(self):
        req_data = {
            "title": "hight",
            "author": "dan",
            "narrator": "narrator",
            "duration": 123456
        }
        s = AudioBook(**req_data)
        self.db.session.add(s)
        self.db.session.commit()
        data = dict(audio_book=self.valid_file)
        resp = self.client.put(f"/api/audio/audio_book/{s.id}", data=data, content_type="multipart/form-data")
        self.assertEquals(resp.status_code, 200)
        data = json.loads(resp.data.decode())
        self.assertEquals(data["audiobook"]["title"], req_data["title"])
        self.assertIsNotNone(data["audiobook"]["uploaded_time"])

    def test_reject_invalidfile_in_upload(self):
        req_data = {
            "title": "hight",
            "author": "dan",
            "narrator": "narrator",
            "duration": 123456
        }
        s = AudioBook(**req_data)
        self.db.session.add(s)
        self.db.session.commit()
        data = dict(audio_book=self.invalid_file)
        resp = self.client.put(f"/api/audio/audio_book/{s.id}", data=data, content_type="multipart/form-data")
        self.assertEquals(resp.status_code, 400)

    def test_reject_upload_for_audio_that_doesnt_exist_in_db(self):
        data = dict(audio_book=self.valid_file)
        resp = self.client.put(f"/api/audio/audio_book/300", data=data, content_type="multipart/form-data")
        self.assertEquals(resp.status_code, 404)

    def test_get_all(self):
        for i in range(5):
            req_data = {
                "title": "hight",
                "author": "dan",
                "narrator": "narrator",
                "duration": 123456
            }
            s = AudioBook(**req_data)
            self.db.session.add(s)
            self.db.session.commit()
        resp = self.client.get("/api/audio/audio_book")
