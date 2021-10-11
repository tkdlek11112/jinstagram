from django.shortcuts import render
from rest_framework.views import APIView
from .models import User
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.response import Response


class Login(APIView):
    def get(self, request):
        return render(request, 'user/login.html')

    def post(self, request):
        email = request.data.get('email', None)
        password = request.data.get('password', None)
        print(email, password)
        if email is None:
            return Response(status=500, data=dict(message='이메일을 입력해주세요'))

        if password is None:
            return Response(status=500, data=dict(message='비밀번호를 입력해주세요'))

        user = User.objects.filter(email=email).first()

        if user is None:
            return Response(status=500, data=dict(message='입력정보가 잘못되었습니다.'))

        if check_password(password, user.password) is False:
            return Response(status=500, data=dict(message='입력정보가 잘못되었습니다.'))

        request.session['loginCheck'] = True
        request.session['email'] = user.email

        return Response(status=200, data=dict(message='로그인에 성공했습니다.'))


class Join(APIView):
    def get(self, request):
        return render(request, 'user/join.html')

    def post(self, request):
        password = request.data.get('password')
        email = request.data.get('email')
        user_id = request.data.get('user_id')
        name = request.data.get('name')

        if User.objects.filter(email=email).exists() :
            return Response(status=500, data=dict(message='해당 이메일 주소가 존재합니다.'))
        elif User.objects.filter(user_id=user_id).exists() :
            return Response(status=500, data=dict(message='사용자 이름 "' + user_id + '"이(가) 존재합니다.'))

        # make_password(password)
        User.objects.create(password=make_password(password),
                            email=email,
                            user_id=user_id,
                            name=name)

        return Response(status=200, data=dict(message="회원가입 성공했습니다. 로그인 해주세요."))


class LogOut(APIView):
    def get(self, request):
        request.session.flush()
        return render(request, 'user/login.html')
