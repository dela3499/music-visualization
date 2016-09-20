import Html exposing ( Html, text, div, span, input, textarea, img, table, tr, th, td, i, p, a )
import Html.Events exposing ( on, targetValue, onClick, onDoubleClick, onInput )
import Html.Attributes exposing ( .. )
import Html.App as Html
import Color exposing ( .. )

import Maybe exposing ( withDefault, andThen )

import CollectionsNg.Array as Array exposing ( Array )
--import Array exposing ( Array )
import Set exposing ( Set )
import Dict exposing ( Dict )
import Random
import Result
import List
import Regex
import String
import Time
import Window
import Mouse
import Task
import Debug

main = img [ src "http://localhost:8080/youtube/9oheyNSELm8" ] []