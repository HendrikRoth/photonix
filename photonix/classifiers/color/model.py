import operator
import sys
from collections import defaultdict
from colorsys import rgb_to_hsv
from pathlib import Path

import numpy as np
from PIL import Image


class ColorModel:
    version = 20181130
    approx_ram_mb = 120
    max_num_workers = 2

    def __init__(self):
        self.colors = {
            # Name: ((red, green, blue), ordering)

            # 'Red':                  (255, 0, 0),
            # 'Yellow':               (255, 255, 0),
            # 'Green':                (0, 255, 0),
            # 'Cyan':                 (0, 255, 255),
            # 'Blue':                 (0, 0, 255),
            # 'Magenta':              (255, 0, 255),

            'Red':                  ((120, 4, 20),      1),
            'Dark orange':          ((162, 70, 21),     2),
            'Orange':               ((255, 124, 0),     3),
            'Pale pink':            ((255, 159, 156),   4),
            'Lemon yellow':         ((255, 250, 0),     5),
            'School bus yellow':    ((255, 207, 0),     6),
            'Green':                ((144, 226, 0),     7),
            'Dark lime green':      ((0, 171, 0),       8),
            'Cyan':                 ((0, 178, 212),     9),
            'Blue':                 ((0, 98, 198),      10),
            'Violet':               ((140, 32, 186),    11),
            'Pink':                 ((245, 35, 148),    12),

            'White':                ((255, 255, 255),   13),
            'Gray':                 ((124, 124, 124),   14),
            'Black':                ((0, 0, 0),         15),
        }

    def predict(self, image_file, image_size=32, min_score=0.005):
        image = Image.open(image_file)
        image = image.resize((1000, 1000), Image.BICUBIC)  # Remove sensor noise/grain
        image = image.resize((image_size, image_size), Image.NEAREST)  # Get the interesting colors without muddying them
        pixels = np.asarray(image)
        pixels = [j for i in pixels for j in i]

        summed_results = defaultdict(int)
        for i, pixel in enumerate(pixels):
            best_color = None
            best_score = 0
            for name, (target, _) in self.colors.items():
                score = self.color_distance(pixel, target)
                if score > best_score:
                    best_color = name
                    best_score = score
            if best_color:
                summed_results[best_color] += 1

        averaged_results = {}
        for key, val in summed_results.items():
            val = val / (image_size * image_size)
            if val >= min_score:
                averaged_results[key] = val

        sorted_results = sorted(averaged_results.items(), key=operator.itemgetter(1), reverse=True)
        return sorted_results

    def color_distance(self, a, b):
        # Colors are list of 3 floats (RGB) from 0.0 to 1.0
        a_h, a_s, a_v = rgb_to_hsv(a[0] / 255, a[1] / 255, a[2] / 255)
        b_h, b_s, b_v = rgb_to_hsv(b[0] / 255, b[1] / 255, b[2] / 255)
        diff_h = 1 - abs(a_h - b_h)
        diff_s = 1 - abs(a_s - b_s) * 0.5
        diff_v = 1 - abs(a_v - b_v) * 0.25
        score = diff_h * diff_s * diff_v
        return score


def run_on_photo(photo_id):
    model = ColorModel()
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
    from photonix.classifiers.runners import results_for_model_on_photo, get_or_create_tag
    photo, results = results_for_model_on_photo(model, photo_id)

    if photo:
        from django.utils import timezone
        from photonix.photos.models import PhotoTag
        photo.clear_tags(source='C', type='C')
        for name, score in results:
            tag = get_or_create_tag(library=photo.library, name=name, type='C', source='C', ordering=model.colors[name][1])
            PhotoTag(photo=photo, tag=tag, source='C', confidence=score, significance=score).save()
        photo.classifier_color_completed_at = timezone.now()
        photo.classifier_color_version = getattr(model, 'version', 0)
        photo.save()

    return photo, results


if __name__ == '__main__':
    if len(sys.argv) != 2:
        print('Argument required: image file path')
        exit(1)

    _, results = run_on_photo(sys.argv[1])

    for result in results:
        print('{} (score: {:0.10f})'.format(result[0], result[1]))
