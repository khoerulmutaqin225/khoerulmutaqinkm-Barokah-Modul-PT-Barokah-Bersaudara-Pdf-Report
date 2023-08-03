# -*- coding: utf-8 -*-

from odoo import models, fields,  _,api
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError
from datetime import datetime
from odoo.tools import date_utils
from datetime import timedelta


class StockPickingInherit(models.Model):
    _inherit = 'stock.picking'

    def _get_default_received_by(self):
        return self.env["res.users"].browse(self.env.uid)

    def button_multiple_Validate(self):
        self.action_done()
        return

    @api.depends('move_lines.quantity_done')
    def _compute_siap_validate(self):
        precision_digits = self.env['decimal.precision'].precision_get('Product Unit of Measure')
        for rec in self:
            no_overquantity = rec.move_lines.filtered(
                lambda move: move.product_uom_qty != 0 and float_compare(move.quantity_done, move.product_uom_qty,
                                                                         precision_rounding=move.product_uom.rounding) == 1
            )
            no_quantities_done = all(
                float_is_zero(move_line.qty_done, precision_digits=precision_digits) for move_line in
                rec.move_line_ids.filtered(lambda m: m.state not in ('done', 'cancel')))

            if no_overquantity or no_quantities_done:
                rec.update({
                    'siap_validate': False
                })

            if not no_overquantity and not no_quantities_done:
                rec.update({
                    'siap_validate': True
                })
            else:
                rec.update({
                    'siap_validate': False
                })
                

    siap_validate = fields.Boolean(
        string="Siap Validate", compute='_compute_siap_validate',readonly=True, default=False, store=True
    )

     
    purchase_id = fields.Many2one(
        'purchase.order',
        string='Nomor PO'
    )
    
    # siap_validate = fields.Boolean(
    #     'siap_validate'
    # )

    second_state = fields.Selection(
        string='Status Order',
        selection=[('onprogress', 'On Progress'), ('transit', 'Transit Ready'), ('nottransit','Barang Stock')],
        default="onprogress",
        readonly=True

    )

    transit_ready_date = fields.Datetime(
        string='Tanggal Ready Barang',
        readonly=True
    )

    received_by = fields.Many2one(
        string='Received By',
        comodel_name='res.users',
        ondelete='restrict',
        default=_get_default_received_by,
        readonly=True
    )
    

    product_id = fields.Many2one( string='Product')
    # product_id = fields.Many2one('product.product', 'Product', related='move_lines.product_id', readonly=True)

    is_editable = fields.Boolean(
        string="Is editable", compute="_compute_is_editable", readonly=True
    )

    # 
    approval_ids = fields.One2many('stock.move', 'approval_id', string='Approval Lines')
   

    def notATransit(self):
        return self.write({
            "second_state":'nottransit',
            "transit_ready_date":False
        })

    def buttonTransit(self):
        return self.write({
            "second_state": "transit",
            "transit_ready_date": fields.Datetime.now
        })
    # Penerima barang
    # penerima_barang = fields.Many2one('res.users',string='Penerima barang')
    sign_stock_penerima = fields.Binary(
        string='sign_stock_penerima',
    )

    # PIC Pembeli
    # pic_pembeli = fields.Many2one('res.users',string='PIC Pembeli')
    sign_pic_pembeli = fields.Binary(
        string='sign_pic_pembeli',
    )

    # Penyiap barang
    # penyiap_barang = fields.Many2one('res.users', string='Penyiap barang')
    sign_penyiap_barang = fields.Binary(
        string='sign_penyiap_barang',
    )    
            
    # @api.depends('move_ids_without_package')
    # def _compute_ttd(self):
    #     for record in self:
    #         if not record.move_ids_without_package:
    #             return{}
    #         else:
    #             record.sign_stock_penerima = record.move_ids_without_package.sign_stock_penerima
                # record.sign_pic_pembeli = record.move_ids_without_package.sign_pic_pembeli
                # record.sign_penyiap_barang = record.move_ids_without_package.sign_penyiap_barang
                # return{}
    # @api.depends('move_ids_without_package')
    # def _compute_ttd(self):
    #     for record in self:
    #         if not record.move_ids_without_package:
    #             return{}
    #         else:
                # record.sign_stock_penerima = record.move_ids_without_package.sign_stock_penerima
                # record.sign_pic_pembeli = record.move_ids_without_package.sign_pic_pembeli
                # record.sign_penyiap_barang = record.move_ids_without_package.sign_penyiap_barang
                # return{}
    # @api.depends('move_ids_without_package')
    # def _compute_ttd(self):
    #     for record in self:
    #         if not record.move_ids_without_package:
    #             return{}
    #         else:
                # record.sign_stock_penerima = record.move_ids_without_package.sign_stock_penerima
                # record.sign_pic_pembeli = record.move_ids_without_package.sign_pic_pembeli
                # record.sign_penyiap_barang = record.move_ids_without_package.sign_penyiap_barang
                # return{}
            
    @api.depends("state")
    def _compute_is_editable(self):
        for rec in self:
            if rec.state in ("first_approved", "approved", "rejected", "done"):
                rec.is_editable = False
            else:
                rec.is_editable = True
                


class StockMoveInherit(models.Model):
    _inherit = 'stock.move'
    

    approval_id = fields.Many2one(
        string='Approval ID',
        comodel_name='stock.picking',
        ondelete='restrict',
    )
    
    @api.onchange('penerima_barang')
    def func_onchange_penerima_barang(self):
        if not self.penerima_barang:
            return{}
        else:
            self.sign_stock_penerima = self.penerima_barang.sign_x
            return{}
    
    @api.onchange('pic_pembeli')
    def func_onchange_pic_pembeli(self):
        if not self.pic_pembeli:
            return{}
        else:
            self.sign_pic_pembeli = self.pic_pembeli.sign_x
            return{}
    
    @api.onchange('penyiap_barang')
    def func_onchange_penyiap_barang(self):
        if not self.penyiap_barang:
            return{}
        else:
            self.sign_penyiap_barang = self.penyiap_barang.sign_x
            return{}
    

    # Penerima barang
    penerima_barang = fields.Many2one('res.users',string='Penerima barang')
    sign_stock_penerima = fields.Binary('sign_stock_penerima')

    # PIC Pembeli
    pic_pembeli = fields.Many2one('res.users',string='PIC Pembeli')
    sign_pic_pembeli = fields.Binary('sign_pic_pembeli')

    # Penyiap barang
    penyiap_barang = fields.Many2one('res.users', string='Penyiap barang')
    sign_penyiap_barang = fields.Binary('sign_penyiap_barang')    
    
    
    actual_supply = fields.Date(
        string='Actual Supply',
        readonly=False,
    )

    arrival_date = fields.Datetime(
        string='Arrival Date',
        readonly=False,
        default=fields.Datetime.now(),
    )
    




class StockMoveInherit(models.Model):
    _inherit = 'stock.move'

    actual_supply = fields.Date(
        string='Actual Supply',
        readonly=False,
    )

    arrival_date = fields.Datetime(
        string='Arrival Date',
        readonly=False,
        default=fields.Datetime.now(),
    )
    
    nomor_do = fields.Many2one(
        'approval',
        string='Nomor Do'
    )

    penerima_do = fields.Char(
        string='Penerima',
        required=False)

    received_by = fields.Char(
        string='Received By',
    )
    
    
    # Penyebab error usage

    # received_by = fields.Many2one(
    #     'res.users',
    #     string='Received By',
    #     related='picking_id.received_by',
    #     readonly=True,
    #     store=True,
    # )

    lokasi_id = fields.Many2one(
        comodel_name='lokasi.lokasi',
        string='Lokasi Supply',
        readonly=True,
    )

    requested_by = fields.Many2one(
        comodel_name="res.users",
        string="Requested by"
    )

    date_start = fields.Date(
        string='Date Start',
        readonly=True,
    )

    nomor_request = fields.Char(
        string='Nomor Request',
        readonly=True,
    )

    name_product = fields.Char(
        string='Product Description',
        readonly=True,
    )

    request_accepted_date = fields.Datetime(
        string="Request Accepted Date",
        readonly=True,
    )

    vessel_id = fields.Many2one(
        'shipping.vessel',
        string='Vessel',
        readonly=True,
    )

    divisi_id = fields.Many2one(
        'hr.department',
        string='Divisi',
        readonly=True,
    )

    code_budget_id = fields.Char(
        string="Code Budget"
    )

    # code_budget_id = fields.Many2one(
    #     comodel_name="code.budget",
    #     string="Code Budget",
    #     readonly=True,
    # )

    specs = fields.Text(string="Specifications", readonly=True, )

    priority_request = fields.Selection(
        string='Priority',
        selection=[('high', 'H'), ('medium', 'M'), ('low', 'L')],
        readonly=True,
    )

    arrival_estimation = fields.Integer(
        string='Days',
        readonly=True,
    )

    status_list = fields.Selection(
        string='Status Type',
        selection=
        [('onprogress', 'On Progress'),
         ('parsial', 'Parsial'),
         ('hold', 'Hold'),
         ('cancel', 'Cancel'),
         ('close', 'Close')],
        readonly=False,
    )

    keterangan_status = fields.Selection(
        selection=[('ready', 'Ready'), ('indent', 'Indent'),
                   ('konfirmasi', 'Konfirmasi'),
                   ('delivery', 'Delivery'),('close', 'Close')],
        string="Keterangan Status",
        readonly=False,
    )

    remark = fields.Char(
        string='Remark',
        readonly=False,
    )
    

    project_id = fields.Char(
        string='Project / Unit'
    )

    # project_id = fields.Many2one(
    #     'project.unit',
    #     string='Project / Unit',
    #     readonly=True,
    # )

    date_done = fields.Datetime('Actual Supply', help="Date at which the transfer has been processed or cancelled.")

    date_done = fields.Datetime('Actual Supply', copy=False, readonly=True,
                                related='picking_id.date_done',
                                store=True,
                                help="Date at which the transfer has been processed or cancelled.")

    vendor_id = fields.Many2one('res.partner', string='Vendor', readonly=True,)

    code_vessel = fields.Char(
        tring='Kode Kapal'
    )

    # code_vessel = fields.Char(
    #     tring='Kode Kapal',
    #     related='vessel_id.code_vessssel',
    #     readonly=True,
    # )

    department_code = fields.Char(
        string='Kode Dep.'
     )

    # department_code = fields.Char(
    #     tring='Kode Dep.',
    #     related='divisi_id.department_code',
    #     readonly=True,
    # )
#
    code_company = fields.Char(
        string='Code-Cop',
        readonly=True,)

    sisa_supply = fields.Integer(
        string='Sisa Supply',
        default=0,
        store=True,
    )
    
    
class Approval(models.Model):
    _name = "approval"
    _description = "Print Out DO Wizard"

    name = fields.Char(
        string="Nomor DO"
    )
    
    purchase_id = fields.Many2one(
        'purchase.order',
        string='Nomor Po'
    )   
        
    
class algoritma_pembelian_report_wizard(models.TransientModel):
    _name = 'stock.picking.report.wizard'
    _description ="Print Stock Picking"
    
    nomor_do = fields.Many2one(
        'approval', 
        string='Nomor_wo'
    )
    
    purchase_id = fields.Many2one(
        related='nomor_do.purchase_id',
        string="Nomor PO",
    )
    
    def debug_v2(self):
        print("dHello World")
        domain =[]
        test=[]
        nomor_do = self.nomor_do
        purchase_id =self.purchase_id
        
        if nomor_do:
            domain += [('nomor_do', '=', nomor_do.id)]
            test += [('name', '=', nomor_do.name)]
            
        stocks = self.env['stock.move'].search_read(domain)
        testt = self.env['approval'].search_read(test)
        print("stocks", stocks)
        print("testt", testt)
        
        data={
            'form':self.read()[0],
            'stocks': stocks,
            'testt': testt
        }
        return self.env.ref('barokah_module.actions_print_stock_picking').report_action(self, data=data)

    
    