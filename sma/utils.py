ROLES = (
    ('staff', 'Staff'),
    ('mentor', 'Mentor'),

)
ATTENDANCE = (
    ('present', 'Present'),
    ('absent', 'Absent'),
    ('late', 'Late'),
)

from io import BytesIO
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
#from django.urls import reverse


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.replace(u'\ufeff', '').encode("latin-1")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None