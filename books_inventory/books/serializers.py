from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from django.contrib.auth.models import User
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.contrib.auth.password_validation import validate_password

from .models import Book, Borrower




class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'first_name', 'last_name')
        write_only_fields = ('password',)
        read_only_fields = ('id',)
        extra_kwargs = {
            'username' : {'validators': [UnicodeUsernameValidator()],},
            'first_name' : {'required': True},
            'last_name' : {'required': True},
            'email' : {'required': True}
        }

    def create(self, validated_data):
        user = User.objects.create(username=validated_data['email'], email=validated_data['email'], first_name=validated_data['first_name'], last_name=validated_data['last_name'])
        user.set_password(validated_data['password'])
        user.save()
        return user


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ('id', 'book_name', 'author', 'book_count')


class BorrowerSerializer(serializers.ModelSerializer):
    book_name = serializers.SerializerMethodField()
    borrower_name = serializers.SerializerMethodField()

    class Meta:
        model = Borrower
        # fields = ('id', 'user', 'book', 'borrow_date' )
        fields = ('id', 'user',  'borrower_name', 'book', 'book_name', 'borrow_date' )
        # read_only_fields = ('id', 'borrow_date', 'borrowed_book', 'borrower')

    def get_book_name(self, obj):
        return obj.book.book_name

    def get_borrower_name(self, obj):
        if obj.user:
            return obj.user.first_name +' '+ obj.user.last_name


    def create(self, validated_data):
        book_obj = validated_data['book']

        if book_obj.book_count > 1:
            try:
                borrow_details = Borrower.objects.create(**validated_data)
                book_obj.book_count -= 1
                book_obj.save()
            except Exception as e:
                print(e)
        else:
            raise serializers.ValidationError({'book_count':'Selected book not available'})
        return borrow_details
