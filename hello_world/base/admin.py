# Standard Library
import csv

# Third Party Stuff
from django.http import HttpResponse


class ExportCsvMixin(object):
    export_fields = []

    def get_file_name(self, request):
        return self.model._meta

    def get_headers(self, request):
        export_fields = self.get_export_fields(request)

        fields = export_fields.keys()
        headers = [export_fields[field] for field in fields]

        return headers

    def get_export_fields(self, request):
        return self.export_fields

    def export_as_csv(self, request, queryset):
        file_name = self.get_file_name(request)
        field_names = self.get_export_fields(request)
        headers = self.get_headers(request)

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = f"attachment; filename={file_name}.csv"
        writer = csv.writer(
            response,
            dialect="excel",
            delimiter=",",
            quotechar='"',
            quoting=csv.QUOTE_ALL,
        )

        writer.writerow(headers)
        for obj in queryset:
            csv_row = []
            for field_name in field_names:
                modeladmin_field = getattr(self, field_name, None)
                if callable(modeladmin_field):
                    func = getattr(self, str(field_name))
                    value = func(obj)
                else:
                    value = getattr(obj, field_name)
                csv_row.append(value)
            writer.writerow(csv_row)

        return response

    export_as_csv.short_description = "Export Selected"
