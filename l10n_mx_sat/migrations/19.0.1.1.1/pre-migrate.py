# Copyright 2026 Gray Matter Logic
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    """Rewrite stored voucher types to SAT codes.

    Metadata files keep ``Ingreso``, ``Egreso``, ``Nómina``, ``Pago`` and
    ``Traslado``. Odoo 19 raises ``ValueError`` when those rows are read as
    a selection, which breaks the document list on upgrade. The same
    first-letter rule as ``_normalize_voucher_type`` is applied in SQL so
    the ORM never has to read the legacy values. Anything else becomes NULL.
    """
    cr.execute(
        """
        UPDATE l10n_mx_sat_document
           SET voucher_type = CASE upper(left(btrim(voucher_type), 1))
                WHEN 'I' THEN 'I'
                WHEN 'E' THEN 'E'
                WHEN 'P' THEN 'P'
                WHEN 'N' THEN 'N'
                WHEN 'T' THEN 'T'
                ELSE NULL
            END
         WHERE voucher_type IS NOT NULL
           AND voucher_type NOT IN ('I', 'E', 'P', 'N', 'T')
        """
    )
    _logger.info(
        "l10n_mx_sat: normalized %s voucher_type values while upgrading from %s",
        cr.rowcount,
        version,
    )
