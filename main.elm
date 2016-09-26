port module MusicAnalyzer exposing (..)

import Html exposing ( Html, iframe, text, div, span, input, textarea, img, table, tr, th, td, i, p, a )
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

import Json.Encode as Json


main = 
  Html.program
    { init = ( initialModel, initCmd )
    , view = view
    , update = update
    , subscriptions = subscriptions
    }


initCmd = 
  Cmd.none


subscriptions: Model -> Sub Msg
subscriptions model = 
  Sub.none


type ID
  = YouTube String 
  | Error String 
  | NoID


type alias Model = 
  { id: ID
  }


initialModel = 
  { id = NoID
  }


type Msg
  = SetID String


update: Msg -> Model -> ( Model, Cmd Msg )
update msg model =
  case msg of
    SetID string -> 
      ( { model | id = getID string }, Cmd.none )


view : Model -> Html Msg
view model =
  div
    [ ]
    [ input 
        [ placeholder "Put in a Youtube URL!"
        , onInput ( \string -> SetID string )
        ]
        [ ]
    , model |> toString |> text 
    , showImage model.id
    --, div [ id "video-placeholder" ] []
    , showVideo model.id
    ]


showVideo modelID = 
  case modelID of
    YouTube videoID -> 
      iframe 
        [ id "elm-player"
        , width 600
        , height 390
        , src ("http://www.youtube.com/embed/" ++ videoID ++ "enablejsapi=1")
        , style [ ("border", "0") ]
        , property "type" (Json.string "text/html")
        ]
        []      
    Error _ -> 
      div [] [] 
    NoID -> 
      div [] []




showImage id = 
  case id of 
    YouTube videoID -> 
      img [ src ( serverBaseUrl ++ videoID ) ] []
    Error string -> 
      text string
    NoID -> 
      text "Paste in a URL from Youtube!"


----------------------------------------UTILS

youtubeBaseUrl = "https://www.youtube.com/watch?v="


serverBaseUrl = "http://localhost:8080/youtube/"


getID string = 
  let isYouTubeUrl = String.startsWith youtubeBaseUrl string
      id = string |> String.split "?v=" |> getLast
  in 
    if isYouTubeUrl then
      case id of 
        Just string -> 
          YouTube string
        Nothing -> 
          NoID
    else
      NoID


getLast xs = 
  xs
  |> List.reverse
  |> List.head