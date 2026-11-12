from datetime import datetime
from flask import Blueprint, render_template, request, Response, send_from_directory, current_app
from app.models import FarmSettings
from app.services.export_service import ExportService

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    settings = FarmSettings.query.first()
    return render_template('index.html', settings=settings)

@main_bp.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(current_app.config['UPLOAD_FOLDER'], filename)

@main_bp.route('/reports/export')
def export_report():
    report_type = request.args.get('type', 'animal_inventory')
    fmt = request.args.get('format', 'csv')
    start_str = request.args.get('start_date')
    end_str = request.args.get('end_date')
    species_id = request.args.get('species_id', type=int)

    start_date = datetime.strptime(start_str, '%Y-%m-%d').date() if start_str else None
    end_date = datetime.strptime(end_str, '%Y-%m-%d').date() if end_str else None

    title, headers, rows = ExportService.fetch_report_data(report_type, start_date, end_date, species_id)
    settings = FarmSettings.query.first()

    if fmt == 'csv':
        csv_content = ExportService.generate_csv_string(headers, rows)
        filename = f"agripulse_{report_type}_{datetime.now().strftime('%Y%m%d')}.csv"
        return Response(
            csv_content,
            mimetype='text/csv',
            headers={'Content-Disposition': f'attachment; filename={filename}'}
        )
    else:
        return render_template(
            'report_print.html',
            title=title,
            headers=headers,
            rows=rows,
            settings=settings,
            generated_on=datetime.now().strftime('%Y-%m-%d %H:%M')
        )