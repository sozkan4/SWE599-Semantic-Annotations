from django.shortcuts import render, redirect
from .models  import User, Post, Comment, Contact
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from datetime import date
from django.urls import reverse_lazy, reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
import requests
import json
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
import uuid
import os
import environ
import requests
from .models import Tag
from django.http import JsonResponse
from django.utils.text import slugify


# read environment variables
current_directory = os.getcwd()
env = environ.Env()
environ.Env.read_env('/app/core/.env')



# Create your views here.
def home(request):
    if 'user' in request.session:
        current_user = request.session['user']
        user_posts = Post.objects.all().order_by('-id')
        param = {'current_user': current_user, 'user_posts': user_posts}
        return render(request, 'blogs.html', param)
    else:
        feature_post =  Post.objects.all().order_by('-id')[:3]
        param = {'feature_post': feature_post}
        return render(request, 'home.html', param)


def view_post(request, post_title):
    get_post = Post.objects.get(title=post_title)
    all_rel_posts = Post.objects.filter(user__first_name=get_post.user)
    post_comments = get_post.comment_set.all().order_by('-id')
    liked = False
    try:
        if get_post.likes.filter(first_name=request.session['user']).exists():
            liked = True
    except:
        return redirect('home')

    # Fetch the tags associated with the post
    tags = get_post.tags.all()

    # Fetch the wikidata explanations for the tags
    wikidata_explanations = []
    for tag in tags:
        wikidata_explanations.extend(get_wikidata_explanations(tag.wikidata_id))

    # Get the web link of the post
    web_link = get_post.web_link

    param = {
        'post_data': get_post,
        'all_posts': all_rel_posts,
        'post_comments': post_comments,
        'liked': liked,
        'tags': tags,
        'wikidata_explanations': wikidata_explanations,
        'web_link': web_link,
    }
    return render(request, 'post.html', param)



def get_wikidata_explanations(wikidata_id):
    WIKIDATA_API_URL = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbgetentities",
        "ids": wikidata_id,
        "format": "json",
        "languages": "en",
        "props": "labels|descriptions",
    }
    response = requests.get(WIKIDATA_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        entities = data.get('entities', {})
        entity = entities.get(wikidata_id, {})
        label = entity.get('labels', {}).get('en', {}).get('value', '')
        description = entity.get('descriptions', {}).get('en', {}).get('value', '')
        explanation = {
            'label': label,
            'description': description,
            'concepturi': f'https://www.wikidata.org/wiki/{wikidata_id}',
        }
        return [explanation]  # Return as a single-item list for compatibility

    return []

def like_post(request, post_title):
    user = User.objects.get(first_name=request.session['user'])
    post = Post.objects.get(title=post_title)
    liked = False
    if post.likes.filter(first_name=request.session['user']).exists():
        post.likes.remove(user) 
        liked = False
    else:
        post.likes.add(user)
        liked = True
    return HttpResponseRedirect(reverse('view_post', args=[str(post_title)]))


def delete_post(request, post_title):
    get_post = Post.objects.get(title=post_title)
    get_post.delete()
    messages.success(request, 'Post has been deleted succsfully.')
    return redirect(f'/profile/{get_post.user.first_name}')

def update_post(request, post_title):
    if request.method == 'POST':
        get_post = Post.objects.get(title=post_title)
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image')
        get_post.title = title
        get_post.content = content
        get_post.image = image
        get_post.save()
        return redirect(f'/post/{get_post.title}')
    else:
        return redirect('home')



def view_profile(request, user):
    try:
        user_obj = User.objects.get(first_name=user)
    except ObjectDoesNotExist:
        return HttpResponse('User does not exists.')

    user_posts = user_obj.post_set.all().order_by('-id')
    lis = []
    for post in user_posts:
        lis.append(post.likes.count())
    total_post_likes = sum(lis)

    param = {'user_posts': user_posts, 'user_data': user_obj, 'total_post_likes': total_post_likes}
    try:
        return render(request, 'profile.html', param)
    except:
        messages.warning(request, f"You have to login before access {user}'s profile.")
        return redirect('home')


def update_profile(request, current_user):
    if request.method == 'POST':
        get_user = User.objects.get(first_name=current_user)

        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        mail = request.POST.get('mail')
        bio = request.POST.get('bio')


        get_user.first_name = fname
        get_user.last_name = lname
        get_user.email = mail
        get_user.bio = bio
        get_user.save()
        return redirect(f'/profile/{get_user.first_name}')
    else:
        return redirect('profile')


def change_image(request, user):
    get_user = User.objects.get(first_name=user)
    new_pic = request.FILES['image']

    get_user.profile_pic = new_pic
    get_user.save()
    messages.success(request, 'Profile Picture updated succsfully.')
    return redirect(f'/profile/{get_user.first_name}')


def settings(request, user):
    get_user = User.objects.get(first_name=user)


    if request.method == 'POST':
        pwd1 = request.POST['pwd1']
        pwd2 = request.POST['pwd2']
        email = request.POST['mail']


        if (pwd1 and pwd2) and not email:
            if pwd1==pwd2:
                get_user.password = pwd1
                get_user.save()
                messages.success(request, 'Password saved succesfully.')
            else:
                messages.warning(request, 'Password are not same.')
        elif email and not (pwd1 and pwd2):
            get_user.email = email
            get_user.save()
            messages.success(request, 'Email saved succesfully.')
        elif (pwd1 and pwd2) and email:
            if pwd1==pwd2:
                get_user.password = pwd1
                get_user.email = email
                get_user.save()
                messages.success(request, 'Password and Email saved succesfully.')
            else:
                messages.warning(request, 'Password are not same.')

    param = {'user_data': get_user}
    return render(request, 'profile_setting.html', param)



def delete_user(request, user):
    if request.method == 'POST':
        get_user = User.objects.get(first_name=user)

        firstName = request.POST.get('first_name')
        if firstName == get_user.first_name:
            get_user.delete()
            del request.session['user']
            return redirect('home')

    return HttpResponseRedirect(reverse('settings', args=[str(user)]))


def write_post(request):
    if request.method == 'POST':
        post_title = request.POST.get('title')
        post_content = request.POST.get('content')
        web_link = request.POST.get('webLink')
        tag_names = request.POST.get('tags').split(',')

        # Create tags and fetch Wikidata explanations
        tags = []
        for tag_name in tag_names:
            tag, created = Tag.objects.get_or_create(name=tag_name.strip())
            tags.append(tag)
            if created:
                tag.wikidata_explanations = get_wikidata_explanations(tag_name)
                tag.save()

        # Save the post with created tags
        get_user = User.objects.get(first_name=request.session['user'])
        create_post = Post(user=get_user, title=post_title, content=post_content, web_link=web_link)
        create_post.save()
        create_post.tags.set(tags)

        return render(request, 'create_post.html', {'tags': tags})
    
    else:
        return render(request, 'create_post.html')





def post_created(request):
    if request.method == 'POST':
        post_title = request.POST.get('title')
        post_content = request.POST.get('content')
        get_user = User.objects.get(first_name=request.session['user'])
        slug = slugify(post_title)  # Generate a unique slug based on the post title
        
        # Retrieve tags from the form submission
        tags_input = request.POST.get('tags')
        tags_list = [tag.strip() for tag in tags_input.split(',') if tag.strip()]
        
        # Get existing tags from the database
        existing_tags = Tag.objects.filter(name__in=tags_list)
        
        create_post = Post(user=get_user, title=post_title, content=post_content, creation_date=date.today(), slug=slug)
        create_post.save()
        
        # Add existing tags to the post
        create_post.tags.add(*existing_tags)
        
        messages.success(request, 'Post has been created successfully.')
        return redirect('write_post')
    else:
        tags = Tag.objects.all()
        context = {
            'tags': tags
        }
        return render(request, 'create_post.html', context)



def search(request):
    query = request.GET.get('query')
    search_user_posts = Post.objects.filter(user__first_name__icontains=query)
    search_title = Post.objects.filter(title__icontains=query)
    search_content = Post.objects.filter(content__icontains=query)
    search_result = search_title.union(search_content,search_user_posts)

    param = {'search_result': search_result, 'search_term':query}
    return render(request, 'search.html', param)


def signup(request):
    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        mail = request.POST.get('mail')
        pwd = request.POST.get('pwd')
        bio = request.POST.get('bio')

        create_user = User(first_name=fname, last_name=lname, email=mail, password=pwd, bio=bio)
        if not User.objects.filter(email=mail).exists():
            create_user.save()
            messages.success(request, 'Your account has been created succsfully.')
            return redirect('home')
        else:
            messages.error(request, 'This User is already exists.')
            return redirect('home')


    else:
        return redirect('home')


def login(request):
    if request.method == 'POST':
        mail = request.POST.get('mail')
        pwd = request.POST.get('pwd')

        check_user = User.objects.filter(email=mail, password=pwd)
        if check_user:
            request.session['user'] = check_user.first().first_name
            return redirect('home')
        else:
            messages.warning(request, 'Invalid User')
            return redirect('home')
    else:
        return redirect('home')


def logout(request):
    try:
        del request.session['user']
    except:
        return redirect('login')
    return redirect('login')


def contact(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        mail = request.POST.get('mail')
        msg = request.POST.get('msg')


        create_contact = Contact(name=full_name, email=mail, message=msg)
        create_contact.save()
        messages.success(request, 'Your form has been submitted.')
        return redirect("contact")

    else:
        return render(request, 'contact.html')

#Create Comments
def add_comment(request, post_title):
    name = request.session['user']
    comment = request.POST.get('comment')
    post = Post.objects.get(title=post_title)
    if name!="" and comment!="":
        create_comment = Comment(post=post, name=name, comment=comment)
        create_comment.save()
        return HttpResponseRedirect(reverse('view_post', args=[str(post_title)]))


@csrf_exempt
def create_annotation(request):
    if request.method == 'POST':
        # Access the request body
        body = request.body.decode('utf-8')
        annotation = json.loads(body)
        """ if isset annotation['image_selection'] """
        if 'image_selection' in annotation:
            return convert_image_annotation_to_ldp_format(request, annotation)
        else:
            return convert_text_annotation_to_ldp_format(request, annotation)

        return JsonResponse({'status': 'fail'}, safe=False)


def convert_image_annotation_to_ldp_format(request, annotation):
    random_uuid = uuid.uuid4()

    annotation_ldp = {
        "@context": "http://www.w3.org/ns/anno.jsonld",
        "id": annotation['uri'] + "/annotations/" + str(random_uuid),
        "type": "Annotation",
        "motivation": "highlighting",
        "created": timezone.now().isoformat(),
        "target": {
            "source": annotation['image_selection']['src'],
            "selector": {
                "type": "FragmentSelector",
                "conformsTo": "http://www.w3.org/TR/media-frags/",
                "value": "xywh=percent:" + annotation['image_selection']['x'] + "," + annotation['image_selection'][
                    'y'] + "," + annotation['image_selection']['w'] + "," + annotation['image_selection']['h'],
            },
        },
        "body": {
            "type": "TextualBody",
            "value": annotation['text'],
            "format": "text/plain"
        },
        "creator": request.user.id,
    }

    """ send annotation_ldp to ldp server """
    ANNOTATION_URL = env('ANNOTATION_SERVICE_URL') + "/annotations/"
    requests.post(ANNOTATION_URL, json=annotation_ldp)
    return JsonResponse(annotation, safe=False)


def convert_text_annotation_to_ldp_format(request, annotation):
    random_uuid = uuid.uuid4()
    ranges = annotation['ranges'][0]
    referrer = request.META['HTTP_REFERER']
    annotation_ldp = {
        "@context": "http://www.w3.org/ns/anno.jsonld",
        "id": referrer + "/annotations/" + str(random_uuid),
        "type": "Annotation",
        "motivation": "highlighting",
        "created": timezone.now().isoformat(),
        "target": {
            "source": referrer,
            "selector": {
                "type": "RangeSelector",
                "startSelector": {
                    "type": "XPathSelector",
                    "value": ranges['start']
                },
                "endSelector": {
                    "type": "XPathSelector",
                    "value": ranges['end']
                },
                "startOffset": ranges['startOffset'],
                "endOffset": ranges['endOffset']
            }
        },
        "body": {
            "type": "TextualBody",
            "value": annotation['text'],
            "format": "text/plain"
        },
        "creator": request.user.id
    }

    """ send annotation_ldp to ldp server """
    ANNOTATION_URL = env('ANNOTATION_SERVICE_URL') + "/annotations/"
    requests.post(ANNOTATION_URL, json=annotation_ldp)
    return JsonResponse(annotation, safe=False)


def get_annotations(request):
    # read environment variables
    if request.method == 'GET':
        q = request.GET.get('uri')

        annotations = requests.get(env('ANNOTATION_SERVICE_URL') + "/annotations/search?query=" + q).json()
        json = {
            "total": len(annotations),
            "rows": []
        }
        for annotation in annotations:
            if annotation['target']['selector']['type'] == "FragmentSelector":
                selector = annotation['target']['selector']['value']
                x = selector.split('=percent:')[1].split(',')[0]
                y = selector.split('=percent:')[1].split(',')[1]
                w = selector.split('=percent:')[1].split(',')[2]
                h = selector.split('=percent:')[1].split(',')[3]
                json['rows'].append({
                    "image_selection": {
                        "src": annotation['target']['source'],
                        "uri": annotation['target']['source'],
                        "x": x,
                        "y": y,
                        "w": w,
                        "h": h,
                    },
                    "text": annotation['body']['value'],
                })
            else:
                json['rows'].append({
                    "quote": annotation['body']['value'],
                    "ranges": [
                        {
                            "start": annotation['target']['selector']['startSelector']['value'],
                            "startOffset": annotation['target']['selector']['startOffset'],
                            "end": annotation['target']['selector']['endSelector']['value'],
                            "endOffset": annotation['target']['selector']['endOffset']
                        }

                    ],
                    "uri": annotation['target']['source'],
                    "text": annotation['body']['value'],
                })

    return JsonResponse(json, safe=False)