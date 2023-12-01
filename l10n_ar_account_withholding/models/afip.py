from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AfipTablagananciasEscala(models.Model):
    _name = 'afip.tabla_ganancias.escala'
    _rec_name = 'importe_desde'

    importe_desde = fields.Float(
        'Mas de $',
    )
    importe_hasta = fields.Float(
        'A $',
    )
    importe_fijo = fields.Float(
        '$',
    )
    porcentaje = fields.Float(
        'Más el %'
    )
    importe_excedente = fields.Float(
        'S/ Exced. de $'
    )
    tabla_ganancias_id = fields.Many2one('afip.tabla_ganancias.tabla', string='Tabla ganancias', ondelete='cascade')


class AfipTablagananciasAlicuotasymontos(models.Model):
    _name = 'afip.tabla_ganancias.alicuotasymontos'
    _rec_name = 'codigo_de_regimen'

    codigo_de_regimen = fields.Char(
        'Codigo de regimen',
        size=6,
        required=True,
        help='Codigo de regimen de inscripcion en impuesto a las ganancias.'
    )
    anexo_referencia = fields.Char(
        required=True,
    )
    concepto_referencia = fields.Text(
        required=True,
    )
    porcentaje_inscripto = fields.Float(
        '% Inscripto',
        help='Elija -1 si se debe calcular s/escala'
    )
    porcentaje_no_inscripto = fields.Float(
        '% No Inscripto'
    )
    montos_no_sujetos_a_retencion = fields.Float(
    )
    tabla_ganancias_id = fields.Many2one('afip.tabla_ganancias.tabla', string='Tabla ganancias')


class AfipTablaGananciasTabla(models.Model):
    _name = 'afip.tabla_ganancias.tabla'

    name = fields.Char(string='Nombre')
    update_date = fields.Date(string='Fecha de actualización')
    description = fields.Html(string='Descripción')
    escala_ganancias_ids = fields.One2many('afip.tabla_ganancias.escala', 'tabla_ganancias_id', string='Escala ganancias')

    @api.constrains('escala_ganancias_ids')
    def _check_escala(self):
        for rec in self:
            if rec.escala_ganancias_ids:
                importes_desde = rec.escala_ganancias_ids.mapped('importe_desde')
                importes_hasta = rec.escala_ganancias_ids.mapped('importe_hasta')
                minimo_desde = min(importes_desde)
                maximo_hasta = max(importes_hasta)
                if minimo_desde != 0.0:
                    raise ValidationError('El importe mínimo debe ser $0,00.')
                total = sum(importes_hasta) - sum(importes_desde)
                if total != maximo_hasta:
                    raise ValidationError('La escala presenta huecos.')
