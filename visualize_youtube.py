import matplotlib.pyplot as plt
import scipy.spatial.distance as ssd
import numpy as np
import librosa
import PIL
import cProfile
import pydub.utils
import sh
import os

def to_p(x):
    """ --------------------------
        Array Float -> Array Float
        --------------------------
        Given a set of points, return the 
        empirical, one-sided p-values for the distribution.
        Put differently, for each value, return the fraction 
        of points with a lower value.
    """
    hist, bins_ = np.histogram(x, bins = 1000)
    bins = bins_[:-1]
    cdf = np.cumsum(hist) / np.max(np.cumsum(hist)).astype(float)
    return np.interp(x, bins, cdf)

def get_pairs(X):
    """ --------------------------------
        2D Array Float -> 2D Array Float
        --------------------------------
        Given (N_features, N_samples) array, return
        pairwise distance matrix with shape (N_samples, N_samples)
    """
    return ssd.squareform(to_p(ssd.pdist(X.T, 'euclidean')))    

def quad(x):
    """ --------------------------------
        2D Array Float -> 2D Array Float
        --------------------------------
        Given 2D array, repeat in a grid. 
        Mirror once across bottom, and then 
        mirror all across right. 
    """
    top_left = x
    bottom_left = np.flipud(top_left)
    left = np.vstack([top_left, bottom_left])
    right = np.fliplr(left)
    return np.hstack([left, right])

def audio_to_matrix(mp3_filename):
    """ ------------------------
        String -> 2D Array Float
        ------------------------
        Given filename for mp3, return 
        stylized pairwise similarity matrix 
        (where similarity matrix is reflected in 
        each quadrant)
    """
    original_sample_rate = int(pydub.utils.mediainfo(mp3_filename)['sample_rate'])    
    y, sr = librosa.load(mp3_filename, sr = original_sample_rate) # Use original sample rate to avoid (slow) resampling
    S = librosa.feature.melspectrogram(y, sr=sr, n_mels=128, n_fft = 2048 / 20)
    log_S = librosa.logamplitude(S, ref_power=np.max)

    mfcc        = librosa.feature.mfcc(S=log_S, n_mfcc=13)
    delta_mfcc  = librosa.feature.delta(mfcc)
    delta2_mfcc = librosa.feature.delta(mfcc, order=2)
    M = np.vstack([mfcc, delta_mfcc, delta2_mfcc])

    chunks = np.linspace(0, log_S.shape[1], 500).astype(int)

    M_sync = librosa.util.sync(M, chunks)
    M_pair = get_pairs(M_sync)
    X = quad(M_pair[:, :-1][:-1,:])
    return X

def create_image_from_audio(mp3_filename, img_filename):
    """ ------------------------------------------
        String -> String -> SideEffect[FileSystem]
        ------------------------------------------
        Create and save image using audio file.
    """
    mat = audio_to_matrix(mp3_filename)
    im = PIL.Image.fromarray(np.uint8(plt.cm.viridis_r(mat)*255)).resize((200,200)).resize((1000,1000))
    im.save(img_filename)
    
def download(url, mp3_filename):
    """ ------------------------------------------
        String -> String -> SideEffect[FileSystem]
        ------------------------------------------
        Download mp3 from url and save to file.
    """
    if os.path.isfile(mp3_filename):
        sh.rm(mp3_filename)
    sh.youtube_dl(
        url,
        extract_audio = True,
        audio_format = "mp3",
        o = mp3_filename
    )
    
def url_to_img(url, mp3_filename, img_filename):
    """ ----------------------------------------------------
        String -> String -> String -> SideEffect[FileSystem]
        ----------------------------------------------------
        Download mp3 from url to file, and then create and 
        save image from it. 
    """
    download(url, mp3_filename)
    create_image_from_audio(mp3_filename, img_filename)     
    
# create_image_from_audio(
#     '../tmp/song.mp3', 
#     '../tmp/img.png')         