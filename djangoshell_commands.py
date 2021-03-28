# 1
from django.contrib.auth.models import User
user1 = User.objects.create(username='user_1', first_name='Иван', last_name='Петров', password='123')
user2 = User.objects.create(username='user_2', first_name='Jhon', last_name='Doe', password='321')

# 2
from news_paper.models import Author
author1 = Author.objects.create(user_id=user1)
author2 = Author.objects.create(user_id=user2)

# 3
from news_paper.models import Category
cathegory1 = Category.objects.create(category='Спорт')
cathegory2 = Category.objects.create(category='Политика')
cathegory3 = Category.objects.create(category='Фантастика')
cathegory4 = Category.objects.create(category='Непонятное')

# 4
from news_paper.models import Post
post_a1 = Post.objects.create(
    author=author1,
    type='A',
    header='Фантастические приключения бекона',
    text='Spicy jalapeno bacon pork belly ball tip buffalo salami bresaola shank turducken. Pastrami rump beef, doner pig cow chuck meatball ground round. Meatball flank capicola, tongue cow pork tri-tip prosciutto strip steak picanha landjaeger meatloaf. Shoulder cupim short loin kevin salami sirloin filet mignon pork flank bresaola boudin pig. Kevin short loin prosciutto, pork chop ground round leberkas drumstick bresaola. Sausage shankle burgdoggen chislic t-bone jerky.',
)
post_a2 = Post.objects.create(
    author=author1,
    type='A',
    header='Бекон и спорт',
    text='Pastrami jerky pork loin picanha beef ribs ham hock. Prosciutto meatloaf chislic kevin leberkas. Andouille pastrami meatloaf ham hock turducken jerky flank meatball cupim short ribs pork loin cow venison chislic kevin. Brisket kielbasa pork belly turkey, frankfurter kevin hamburger filet mignon t-bone cupim biltong beef ribeye ground round.',
)
post_n1 = Post.objects.create(
    author=author2,
    type='N',
    header='Бекон побеждён!',
    text='Spicy jalapeno bacon pork belly.',
)

# 5
from news_paper.models import PostCategory
pa1_c3 = PostCategory.objects.create(post=post_a1, category=cathegory3)
pa1_c4 = PostCategory.objects.create(post=post_a1, category=cathegory4)
pa2_c1 = PostCategory.objects.create(post=post_a2, category=cathegory1)
pa2_c4 = PostCategory.objects.create(post=post_a2, category=cathegory4)
pn1_c2 = PostCategory.objects.create(post=post_n1, category=cathegory2)
pn1_c4 = PostCategory.objects.create(post=post_n1, category=cathegory4)
pn1_c3 = PostCategory.objects.create(post=post_n1, category=cathegory3)

# 6
from news_paper.models import Comment
com1 = Comment.objects.create(post=post_a1, user=user1, text='Моя статья лучшая!')
com2 = Comment.objects.create(post=post_a1, user=user2, text='А вот и нет!')
com3 = Comment.objects.create(post=post_a2, user=user2, text='Люблю спорт!')
com4 = Comment.objects.create(post=post_n1, user=user1, text='Ничего не понял...')
com5 = Comment.objects.create(post=post_n1, user=user2, text='Bacon shank landjaeger meatball?')

# 7
post_a1.like()
post_a1.like()
post_a1.dislike()
post_a2.like()
post_a2.like()
post_n1.dislike()
post_n1.dislike()
post_n1.dislike()
com1.dislike()
com2.dislike()
com3.like()
com3.like()
com4.like()
com4.like()
com5.dislike()

# 8
author1.update_rating()
author2.update_rating()

# 9
Author.objects.all().order_by('-rating').values('user_id__username', 'rating')[0]

# 10
Post.objects.filter(type=Post.ARTICLE).order_by('-rating').values('creation_time', 'author__user_id__username', 'rating', 'header')[0]
Post.objects.filter(type=Post.ARTICLE).order_by('-rating')[0].priview()

# 11
Comment.objects.filter(post=Post.objects.filter(type=Post.ARTICLE).order_by('-rating')[0]).values('creation_time', 'user', 'rating', 'text')
