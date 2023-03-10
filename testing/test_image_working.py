import numpy as np
import pytest as pt
from module_image_working.detection import Image2Vector


class TestImage2Vector:

    def test_image_without_face(self):
        image = '/home/nikita/PycharmProjects/ProjectVKR/data/test_images/tiger.jpg'
        assert (Image2Vector().get_embedding_face(image) == 999).any()

    def test_image_with_two_and_more_face(self):
        image = '/home/nikita/PycharmProjects/ProjectVKR/data/test_images/more_people.jpg'
        assert (Image2Vector().get_embedding_face(image) < 1).any()

    def test_image_half_face(self):
        image = '/home/nikita/PycharmProjects/ProjectVKR/data/test_images/without_right_part_face.jpg'
        assert (Image2Vector().get_embedding_face(image) < 1).any()

    def test_image_with_glasses_face(self):
        image = '/home/nikita/PycharmProjects/ProjectVKR/data/test_images/with_glasses.jpg'
        assert (Image2Vector().get_embedding_face(image) < 1).any()

    def test_image_with_mask_face(self):
        image = '/home/nikita/PycharmProjects/ProjectVKR/data/test_images/with_mask.jpg'
        assert (Image2Vector().get_embedding_face(image) < 1).any()

    def test_face_90deg(self):
        image = '/home/nikita/PycharmProjects/ProjectVKR/data/test_images/left90.jpg'
        assert (Image2Vector().get_embedding_face(image) < 1).any()

    def test_face_45deg(self):
        image = '/home/nikita/PycharmProjects/ProjectVKR/data/test_images/right45.jpg'
        assert (Image2Vector().get_embedding_face(image) < 1).any()

    def test_front_face(self):
        image = '/home/nikita/PycharmProjects/ProjectVKR/data/test_images/front.jpg'
        assert (Image2Vector().get_embedding_face(image) < 1).any()

    def test_far_face(self):
        image = '/home/nikita/PycharmProjects/ProjectVKR/data/test_images/far_face.jpg'
        assert (Image2Vector().get_embedding_face(image) < 1).any()
