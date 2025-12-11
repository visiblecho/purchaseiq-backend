# receipts/serializers.py
from rest_framework import serializers
from django.utils.dateparse import parse_datetime
from ..models import Receipt, ReceiptItem

class ReceiptItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptItem
        fields = [
            "id",
            "description",
            "tags",
            "raw_entry",
            "quantity",
            "price_per_unit",
            "total_price",
        ]


class ReceiptSerializer(serializers.ModelSerializer):
    items = ReceiptItemSerializer(many=True)

    class Meta:
        model = Receipt
        fields = [
            "id",
            "datetime_raw",
            "datetime_iso_8601",
            "datetime_timezone",
            "datetime_parsed",

            "currency_primary",
            "currency_secondary",
            "currency_exchange_rate",
            "currency_symbol",

            "store_name",
            "store_street",
            "store_number",
            "store_zip",
            "store_city",
            "store_country",

            "total_subtotal",
            "total_tax",
            "total_price",

            "payment_method",
            "items",
        ]
        read_only_fields = ["datetime_parsed"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")

        # auto-parse ISO 8601 string
        iso = validated_data.get("datetime_iso_8601")
        validated_data["datetime_parsed"] = parse_datetime(iso) if iso else None

        receipt = Receipt.objects.create(**validated_data)

        for item in items_data:
            ReceiptItem.objects.create(receipt=receipt, **item)

        return receipt
