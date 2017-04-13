from django.conf import settings
from models import Account, Transaction
from exchange.models import Currency
from rest_framework import serializers
import re


class AccountSerializer(serializers.ModelSerializer):
    currency = serializers.CharField(max_length=3)

    class Meta:
        model = Account
        fields = ("id", "uid", "current_balance", "currency",)
        read_only_fields = ('id', 'uid', 'current_balance')

    def validate_currency(self, value):
        CUR_REGEX = getattr(settings, 'CUR_REGEX', False)
        CURRENCY_LIST = getattr(settings, 'CURRENCY_LIST', False)

        if not re.match(CUR_REGEX, value):
            raise serializers.ValidationError(
                "currency code mus be in ISO 4217 standard")

        if value not in CURRENCY_LIST:
            raise serializers.ValidationError("currency code not allowed")
        return value

    def create(self, validated_data):
        currency = validated_data.pop('currency')
        if Currency.objects.filter(iso_code=currency).exists():
            cur = Currency.objects.filter(iso_code=currency).get()
        else:
            cur = Currency(iso_code=currency)
            cur.save()
        acc = Account(currency=cur)
        acc.save()
        return acc


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ("id", "uid", "running_balance", "currency",)
        extra_kwargs = {'id': {'read_only': True}, 'uid': {
            'read_only': True}, 'running_balance': {'read_only': True}}


class TransactionWithdrawalsSerializer(serializers.Serializer):
    destAccount = serializers.IntegerField(
        max_value=99999999, min_value=10000000)
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=1)

    def validate_destAccount(self, value):
        if not Account.objects.filter(uid=value).exists():
            raise serializers.ValidationError("does not exists")
        return value

    def create(self, validated_data):
        destAccount = validated_data.pop('destAccount')
        amount = validated_data.pop('amount')
        dst = Account.objects.filter(uid=destAccount).get()
        result = dst.withdraw(amount)
        return result


class TransactionDepositSerializer(serializers.Serializer):
    sourceAccount = serializers.IntegerField(
        max_value=99999999, min_value=10000000)
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=1)

    def validate_sourceAccount(self, value):
        if not Account.objects.filter(uid=value).exists():
            raise serializers.ValidationError("does not exists")
        return value

    def create(self, validated_data):
        sourceAccount = validated_data.pop('sourceAccount')
        amount = validated_data.pop('amount')
        src = Account.objects.filter(uid=sourceAccount).get()
        result = src.deposit(amount)
        return result


class TransactionTransfersSerializer(serializers.Serializer):
    sourceAccount = serializers.IntegerField(
        max_value=99999999, min_value=10000000)
    destAccount = serializers.IntegerField(
        max_value=99999999, min_value=10000000)
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, min_value=1)

    def validate(self, data):
        if data['sourceAccount'] == data['destAccount']:
            raise serializers.ValidationError(
                "sourceAccount and destAccount mus be different")
        if Account.objects.filter(uid=data['sourceAccount']).exists():
            acount = Account.objects.filter(uid=data['sourceAccount']).get()
            if not acount.positive_balance(data['amount']):
                raise serializers.ValidationError("sourceAccount Negative  ")

        return data

    def validate_sourceAccount(self, value):
        if not Account.objects.filter(uid=value).exists():
            raise serializers.ValidationError("does not exists")
        return value

    def validate_destAccount(self, value):
        if not Account.objects.filter(uid=value).exists():
            raise serializers.ValidationError("does not exists")
        return value

    def create(self, validated_data):
        print "Create transaction ", validated_data
        sourceAccount = validated_data.pop('sourceAccount')
        destAccount = validated_data.pop('destAccount')
        amount = validated_data.pop('amount')

        src = Account.objects.filter(uid=sourceAccount).get()
        dst = Account.objects.filter(uid=destAccount).get()
        result = src.transfer(dst, amount)

        return result
