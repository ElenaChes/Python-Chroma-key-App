# Chroma key App

A "green screen" replacing program written in Python using OpenCV.<br>
Description: a simple app that takes two images - one with green areas, the other a background image, and outputs an image with the green areas replaced with the background image.

<details>
  <summary><h3>Content</h3></summary>

- [Dependencies](#dependencies)
- [Installation](#installation)
- [Usage](#usage)

</details>
<hr>

# Dependencies

1. Python 3.7.0

The app could work with different versions, but this is the one that was tested.

# Installation

1. Create a new directory, for example `opencv`.
2. Open the directory in your Terminal:

```
cd opencv
```

3. Create a virtual environment:

```
python -m venv opencv-env
```

4. Activate the environment :

```
.\opencv-env\Scripts\activate
```

5. Install needed packages:

```
pip install opencv-contrib-python matplotlib
```

> [!TIP]
> Place the `app.py` file in the same parent folder as `opencv` for ease of use.

# Usage

1. Run the app using the following syntax:

```
python app.py img_filename bk_filename ofilename
```

While:

- `img_filename` - path to an image with a 'green screen'.
- `bk_filename` - path to the background.
- `ofilename` - path to save the edited image, if none is provided it'll be displayed instead.
