from odoo import fields, models, api

class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    recent_sale_order_line = fields.Many2one("sale.order.line", string="Most Recent Order", compute="_compute_recent_sale_order_line", store=True)
    recent_sale_price = fields.Float(related="recent_sale_order_line.price_unit", string="Most Recent Price")
    recent_sale_date = fields.Datetime(related='recent_sale_order_line.order_id.date_order', string="Most Recent Order Date")
    order_date = fields.Datetime(related="order_id.date_order", string="Order Date", store=True)
    @api.depends("order_id.partner_id", "product_id")
    def _compute_recent_sale_order_line(self):
        for record in self:
            record.recent_sale_order_line = None
            customer = record.order_id.partner_id.id
            product = record.product_id.id

            line = self.env["sale.order.line"].search([("order_id.partner_id", '=', customer),
                    ("product_id", '=', product), ("order_id", "!=", record.order_id.id), ("order_id.state", "=", 'sale')
                    ], order="order_date desc", limit=1)

            record.recent_sale_order_line = line.id
