from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from .models import Article
from .serializers import ArticleSerializer
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view #Se necesita para utilizar los decoradores de api_view
from rest_framework.response import Response
from rest_framework import status

#### authenmtication ####
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

#@csrf_exempt #Este decorador permite que un cliente haga POST a nuestro proyecto aun si no tiene
#un token CSRF, esto NO ES RECOMENDABLE pero para probar nuestro ekjemplo servira por ahora


@api_view(['GET', 'POST']) #este decorador servira para hacer uso del rest framewrok
#Se quiere crear una lista de articulos, listar todos los articles
def article_list(request):
	if request.method == 'GET':
		articles = Article.objects.all()
		#many=true se pone cuando se quiere serializar un queryset
		serializer = ArticleSerializer(articles, many=True)
		print(articles) #Articles es un queryset
		#return JsonResponse(serializer.data, safe =False)
		return Response(serializer.data)

	elif request.method == "POST":
		#Si el metodo es un post hacemos un parse al request
		#data=JSONParser().parse(request)
		#Y lo serializamos
		#serializer=ArticleSerializer(data=data)
		serializer=ArticleSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		#Si la data es invalida:
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


#Ahora probaremos a manipular o ver un solo dato, a traves de una url por ejemplo xxx/modificar/1 
#@csrf_exempt
@api_view(['GET','PUT','DELETE'])
def article_detail(request, pk):
	try:
		article = Article.objects.get(pk=pk) #obtenemos solo un objeto de id=pk, pk tendra su valor en el url
	except Article.DoesNotExist:
		return HttpResponse(status=status.HTTP_404_NOT_FOUND) #arrojar un 404 si no existe dicho objeto

	if request.method == 'GET':
		#a diferencia del get de arriba aqui no se necesita many=true debido a que es solo un objetp dict y no un queryset
		serializer = ArticleSerializer(article)
		#En este caso safe dbee ser true (ya es true por defecto) ya que se le esta pasando un object tipo dict (dictionary)
		#Cuando es false se le puede pasar cualquier objeto
		return Response(serializer.data)
	elif request.method == 'PUT':
		#data = JSONParser().parse(request)


		#Necesario que este incluido el article en los argumentos por ser put
		#serializer = ArticleSerializer(article, data=data)

		serializer = ArticleSerializer(article, data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data) #sin status
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	elif request.method == 'DELETE':
		article.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)

#####################################3
### APIviews basadas en clases#######
from rest_framework.views import APIView

class ArticleAPIView_list(APIView):
	def get(self, request):
		articles = Article.objects.all()
		serializer = ArticleSerializer(articles, many=True)
		print(articles)
		return Response(serializer.data)

	def post(self, request):
		serializer=ArticleSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		#Si la data es invalida:
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
#Como vemos la funcion que cum0ple es la misma a la anterior basada en funciones pero se ve mucho mas ordenado 

class ArticleAPIView_detail(APIView):
	def get_object(self, id):
		try:
			return Article.objects.get(id=id) #obtenemos solo un objeto de id=pk, pk tendra su valor en el url
		except Article.DoesNotExist:
			return HttpResponse(status=status.HTTP_404_NOT_FOUND) #arrojar un 404 si no existe dicho objeto

	def get(self, request, id ):
		article=self.get_object(id)
		serializer = ArticleSerializer(article)
		return Response(serializer.data)

	def put(self, request, id):
		article=self.get_object(id)
		serializer = ArticleSerializer(article, data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data) #sin status
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

	def delete(self, request, id):
		article=self.get_object(id)
		article.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)



######generic views and mixins#####
from rest_framework import generics
from rest_framework import mixins

class GenericAPIView(generics.GenericAPIView, mixins.ListModelMixin , mixins.CreateModelMixin, mixins.UpdateModelMixin,
	mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
	serializer_class = ArticleSerializer
	queryset=Article.objects.all()

	#Con este campo lem decimos al programa que buscaremos por el campo llamado id, esto para recuperar obejtos
	#con el objetivo de manipularlos, por ejemplo en PUT
	lookup_field='id'


	#Esto implementa doble tipo de autentificacion, si la de sesion no esta disponible, hara la basica
	
	#authentication_classes=[SessionAuthentication, BasicAuthentication]
	authentication_classes=[TokenAuthentication]
	permission_classes=[IsAuthenticated]

	def get(self, request, id=None):
		if id:
			return self.retrieve(request)
		else:
			return self.list(request)


	def post(self, request):
		return self.create(request)

	def put(self, request, id=None):
		return self.update(request, id)

	def delete(self,request, id):
		return self.destroy(request, id)

######  ViewSETS  ######

from rest_framework import viewsets
from django.shortcuts import get_object_or_404


class ArticleViewSet(viewsets.ViewSet):
	#en lugfar de los metodos get, post, etc.
	#En viewsets se usan list, retrieve, etc.
	def list(self, request): #get la lista de objetos
		articles = Article.objects.all()
		serializer = ArticleSerializer(articles,many=True)
		return Response(serializer.data)

	def create(self, request): #post
		serializer=ArticleSerializer(data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		#Si la data es invalida:
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

	def retrieve(self, request, pk=None): #retrieve es un get pero para cierto
	#dato espeicfico con cierto pk(primary key)
	#Buscar diferencias entre pk y id
		queryset = Article.objects.all()
		article=get_object_or_404(queryset, pk=pk)
		serializer = ArticleSerializer(article)
		return Response(serializer.data)

	def update(self, request, pk=None): #put
		article=Article.objects.get(pk=pk)
		serializer = ArticleSerializer(article, data=request.data)

		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data) #sin status
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


####  Generic VIEWsets  #####

#Por defecto vienen con el metodo get o list
class ArticleGenericViewSet(viewsets.GenericViewSet, mixins.ListModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
	mixins.RetrieveModelMixin, mixins.DestroyModelMixin):
	serializer_class = ArticleSerializer
	queryset=Article.objects.all()


######  MODAL ViewSETS  ######

#Librerias ya importadas mas arriba
#from rest_framework import viewsets
#from django.shortcuts import get_object_or_404


class ModalArticleViewSet(viewsets.ModelViewSet):

	serializer_class=ArticleSerializer
	queryset = Article.objects.all()
	