# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from datetime import datetime
from odoo.tools import date_utils
from datetime import timedelta

import io
from PIL import Image
import base64


class StockPickingInherit(models.Model):
    _inherit = 'res.users'
    
    @api.depends('sign_x')
    def _compute_image_64(self):
        for template in self:
            if template.sign_x:
                template.sign_x = self._compress_image(template.sign_x)

    def _set_image_64(self):
        for template in self:
            if template.sign_x:
                template.sign_x = self._compress_image(template.sign_x)

    def _compress_image(self, image_data):
        # Decode the image data from base64
        image = Image.open(io.BytesIO(base64.b64decode(image_data)))

        if image.mode != 'RGBA':
            image = image.convert('RGBA')
        # Compress the image
        compressed_image = io.BytesIO()
        image.save(compressed_image, format='PNG',optimize=True,quality=60)

        # Encode the compressed image data to base64
        return base64.b64encode(compressed_image.getvalue())

    sign_x = fields.Binary(
        compute='_compute_image_64', inverse='_set_image_64',
        store=True
    )