# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from models import Account, Transaction
from serializers import AccountSerializer, TransactionSerializer
from serializers import TransactionWithdrawalsSerializer, TransactionDepositSerializer, TransactionTransfersSerializer


class AccountViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class TransactionViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer


@api_view(['POST'])
def accounts(request, format=None):
    if request.method == 'POST':
        data = request.data
        if len(data) > 0:
            serializer = AccountSerializer(data=data)
            if serializer.is_valid():
                try:
                    account = serializer.save()
                    return Response({
                        "ererror": False,
                        "data": {"accountNumber": account.uid},
                    })
                except Exception as e:
                    return Response({
                        "ererror": True,
                        "code": "50000",
                        "message": "Server error",
                    })
            else:
                return Response({
                    "ererror": True,
                    "code": "40000",
                    "message": serializer.errors,
                })
        else:
            return Response({
                "ererror": True,
                "code": "40000",
                "message": "not valid params",
            })



@api_view(['POST'])
def transactions(request, format=None):
    if request.method == 'POST':
        data = request.data
        if 'sourceAccount' in data and 'amount' in data and not 'destAccount' in data:
            serializer = TransactionDepositSerializer(data=data)
            if serializer.is_valid():
                try:
                    transfer = serializer.save()
                    return Response({
                        "ererror": False,
                        "data": { "transactionId":transfer[0]},
                    })
                except Exception as e:
                    return Response({
                        "error": True,
                        "code": "50000",
                        "message": "Server error",
                    })
            else:
                return Response({
                    "error": True,
                    "code": "40000",
                    "message": serializer.errors,
                })
        elif 'destAccount' in data and 'amount' in data and not 'sourceAccount' in data:
            serializer = TransactionWithdrawalsSerializer(data=data)
            if serializer.is_valid():
                try:
                    transfer = serializer.save()
                    return Response({
                        "error": False,
                        "data": {"transactionId": transfer[0]},
                    })
                except Exception as e:
                    return Response({
                        "error": True,
                        "code": "50000",
                        "message": "Server error",
                    })
            else:
                return Response({
                    "error": True,
                    "code": "40000",
                    "message": serializer.errors,
                })
        elif 'sourceAccount' in data and 'destAccount' in data and 'amount' in data:
            serializer = TransactionTransfersSerializer(data=data)
            if serializer.is_valid():
                try:
                    transfer = serializer.save()
                    return Response({
                        "error": False,
                        "data":{"transactionId":transfer[0]},
                    })
                except Exception as e:
                    return Response({
                        "error": True,
                        "code": "50000",
                        "message": "Server error",
                    })
            else:
                return Response({
                    "error": True,
                    "code": "40000",
                    "message": serializer.errors,
                })
        else:
            return Response({
                "error": True,
                "code": "40000",
                "message": "not valid params",
            })
