# Social Media Application

This is a social media application built using the Django framework. It includes features such as user authentication, posting, liking posts, following users, and searching for users. The application provides a platform for users to share posts and interact with each other.

## Features

- **User Authentication**: Sign up, sign in, and log out functionalities.
- **Profile Management**: Users can view and edit their profiles.
- **Post Creation**: Users can upload images with captions.
- **Feed**: Users can view posts from people they follow.
- **Like Posts**: Users can like and unlike posts.
- **Follow/Unfollow Users**: Users can follow and unfollow other users.
- **Search**: Users can search for other users.
- **Suggestions**: Users receive suggestions for new people to follow.

## Requirements

- Python 3.x
- Django
- Other dependencies specified in `requirements.txt`

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/social-media-app.git
   cd social-media-app
   ```

2. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

3. Apply migrations:
   ```bash
   python manage.py migrate
   ```

4. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

6. Access the application at `http://127.0.0.1:8000/`.

## Code Overview

### Views

#### Index View
Displays the user's feed with posts from people they follow and suggests new users to follow.

```python
@login_required(login_url='signin')
def index(request):
    # Fetching user information and generating feed and suggestions
    ...
    return render(request, 'index.html', context)
```

#### Profile View
Displays the profile page of a user with their posts, follower count, and following count.

```python
@login_required(login_url='signin')
def profile(request, pk):
    # Fetching profile information and user's posts
    ...
    return render(request, 'profile.html', context)
```

#### Search View
Allows users to search for other users by username.

```python
@login_required(login_url='signin')
def search(request):
    # Handling user search queries
    ...
    return render(request, 'search.html', context)
```

#### Follower View
Handles following and unfollowing users.

```python
@login_required(login_url='signin')
def follower(request):
    # Managing followers
    ...
    return redirect('/profile/' + user)
```

#### Like Post View
Handles liking and unliking posts.

```python
@login_required(login_url='signin')
def like_post(request):
    # Handling post likes
    ...
    return redirect('/')
```

#### Signup View
Handles user registration.

```python
def signup(request):
    # Handling user signup
    ...
    return redirect('signin')
```

#### Upload View
Allows users to upload new posts.

```python
@login_required(login_url='signin')
def upload(request):
    # Handling new post uploads
    ...
    return redirect('/')
```

#### Settings View
Allows users to update their profile settings.

```python
@login_required(login_url='signin')
def setting(request):
    # Handling profile settings updates
    ...
    return render(request, 'setting.html', {'user_profile': user_profile})
```

#### Signin View
Handles user login.

```python
def signin(request):
    # Handling user signin
    ...
    return redirect('index')
```

#### Logout View
Handles user logout.

```python
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')
```

## Models

- **User**: Django's built-in User model.
- **Profile**: Extends the User model with additional attributes like profile image, bio, and location.
- **Post**: Represents a user's post with an image and caption.
- **LikePost**: Represents likes on posts.
- **FollowerCount**: Represents follower relationships between users.

## Contribution

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any inquiries or issues, please open an issue on GitHub or contact me at Abelmekonn@gmail.com.

---

Enjoy using the social media application!
