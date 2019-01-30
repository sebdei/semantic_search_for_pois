<template>
  <div>
    <div v-if="disableSearchOptionsProp && listOfRecommendations.length === 0" />

    <div v-else>
      <template v-if="!disableSearchOptions">
        <div class="header2 pt-5">
          <h2 class="header-text text-center">
            Choose your option
          </h2>
        </div>
        <div class="weather-distances-box mt-5">
          <form>
            <div class="form-check">
              <h4>
                Radius
              </h4>
              <div class="mt-5 my-3 mb-5">
                <vue-slider class="slider" formatter="{value} km" :max="25" v-model="radius"></vue-slider>
              </div>
              <div class="weather">
                <h4>
                  Weather options
                </h4>
                <div class="weather-element py-3">
                  <div class="onoffswitch">
                    <input type="checkbox" name="consider-weather" class="onoffswitch-checkbox" id="consider-weather" v-model="considerWeather">
                    <label class="onoffswitch-label" for="consider-weather">
                        <span class="onoffswitch-inner"></span>
                        <span class="onoffswitch-switch"></span>
                    </label>
                  </div>
                  <div class="mb-3">
                    Consider weather
                  </div>
                </div>
                <div class="weather-element py-3">
                  <div class="onoffswitch">
                    <input type="checkbox" name="force-bad-weather" class="onoffswitch-checkbox" id="force-bad-weather" v-model="forceBadWeather">
                    <label class="onoffswitch-label" for="force-bad-weather">
                        <span class="onoffswitch-inner"></span>
                        <span class="onoffswitch-switch"></span>
                    </label>
                  </div>
                  <div class="mb-3">
                    Force bad weather
                  </div>
                </div>
              </div>
            <div class="go-button">
              <button type="button" @click="storeAndFetchSearchOptions(radius, considerWeather, forceBadWeather)" class="btn blue btn-lg btn-block">Go!</button>
            </div>
          </div>
        </form>
      </div>
      </template>
      <template v-else>
        <div class="header pt-5" v-if="recommendationType">
          <h2 class="header-text text-center">
            Your personal recommendations
          </h2>
          <h5 class="recommendation-type" v-if="recommendationType === 'content_based'">
            ...based on your input
          </h5>
          <h5 class="recommendation-type" v-if="recommendationType === 'collaborative_filtering'">
            ...based on other user preferences
          </h5>
        </div>
        <div class="poi-list">
          <div v-for="recommendation in listOfRecommendations" class="poi-item" @click="goToDetailPoiRoute(recommendation.id)" :key="recommendation.id">
            <h5 class="font-weight-bold">
              {{ recommendation.name }}
            </h5>
            <div class="teaser-text-wrapper">
              <div class="teaser-text">
                {{ recommendation.source.text }}
              </div>
            </div>
            <div class="distance-box float-right" @click="navigateTo(recommendation.lat, recommendation.long)">
              <div>
                <i class="fas fa-map-marker-alt fa-icon"></i>
              </div>
              <span>
                {{ recommendation.distance}} km
              </span>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

import vueSlider from 'vue-slider-component';

import { L } from 'vue2-leaflet';

import { calcDistance, navigateTo } from '@/service/osm-service'
import { getCookie, setCookie } from '@/service/cookie-service'

export default {
  props: ['disableSearchOptionsProp'],
  components: {
    vueSlider
  },
  data () {
    return {
      berlinMainTrainstationLeaflet: L.latLng(52.525084, 13.369402), // for demo purpose: use berlin station as start point
      considerWeather: false,
      disableSearchOptions: false,
      forceBadWeather: false,
      listOfRecommendations: [],
      recommendationType: '',
      radius: 5
    }
  },
  mounted () {
    if (!getCookie('user_id')) {
      this.$router.push({ path: `/` })
    } else if (this.disableSearchOptionsProp) {
      // getValues from cookie for demonstration purpose!!
      this.fetchRecommendations(getCookie('radius'), getCookie('considerWeather'), getCookie('forceBadWeather'))
    }
  },
  methods: {
    fetchRecommendations: async function (radius = 20, considerWeather = false, forceBadWeather = false) {
      let host = window.location.hostname
      let queryParam = {
        considerWeather: considerWeather,
        forceBadWeather: forceBadWeather,
        lat: 52.525084,
        long: 13.369402,
        radius: radius,
        weatherAPI: false,
        userId: getCookie('user_id')
      }

      let response = await axios.get(`http://${host}:5000/points_of_interests/personal_recommendations/`+
        `${queryParam.userId}/${queryParam.lat}/${queryParam.long}/${queryParam.radius}/${queryParam.considerWeather}/${queryParam.forceBadWeather}`)

      this.recommendationType = response.data.recommendation_type
      let listOfRecommendations = response.data.recommendations

      this.listOfRecommendations = listOfRecommendations.map((recommendation) => {
        recommendation.distance = calcDistance(this.berlinMainTrainstationLeaflet, recommendation.lat, recommendation.long)
        recommendation.source.text = recommendation.source.text.replace(/\s{2,}/g, '')

        return recommendation
      })

      this.disableSearchOptions = true
    },
    goToDetailPoiRoute: function (id) {
      this.$router.push({ path: `/points_of_interests/${id}` })
    },
    storeAndFetchSearchOptions: function (radius, considerWeather, forceBadWeather) {
      // demonstration purpose!
      setCookie('radius', radius)
      setCookie('considerWeather', considerWeather)
      setCookie('forceBadWeather', forceBadWeather)

      this.fetchRecommendations(radius, considerWeather, forceBadWeather)

      this.disableSearchOptions = true
    },
    navigateTo: navigateTo
  }
}
</script>

<style scoped>
.header {
  height: 100%;
  background-color: #463E3C;
  color: white;
}

.recommendation-type {
  text-align: center;
}

.poi-item {
  /* background-color: #766d6c; */
  min-height: 180px;
  padding: 30px;
  border-top: 1px solid;
}

.poi-item:nth-child(even) {
  /* background-color: #463E3C; */
}

.street {
  display: inline-block;
  width: 75%;
}

.distance-box {
  display: inline-block;
  padding: 5px;
  text-align: center;
  border-radius: 7px;
  border: 1px solid rgba(0,0,0,0.23);
  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);
}

.teaser-text {
  font-family: "Droid Serif";
  display: -webkit-box;
  height: 78px;
  -webkit-line-clamp: 4;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 14px;
  font-style: normal;
  font-variant: normal;
  line-height: 20px;
  text-align: justify;
}

.teaser-text-wrapper {
  display: inline-block;
  width: 75%;
}

.fa-icon{
  color: #e44802
}


.header2 {
  height: 150px;
  background-color: #463E3C;
  color: white;
}

.form-check {
  padding: 1.25em;
}

.slider >>> .vue-slider-tooltip {
  border: 1px solid #473e3c;
  background-color: #473e3c;
}

.slider >>> .vue-slider-process {
  background-color: #473e3c;
}

.weather-element {
  display: flex;
}

.onoffswitch {
  margin-right: 20px;
    position: relative; width: 83px;
    -webkit-user-select:none; -moz-user-select:none; -ms-user-select: none;
}
.onoffswitch-checkbox {
    display: none;
}
.onoffswitch-label {
    display: block; overflow: hidden; cursor: pointer;
    border: 2px solid #999999; border-radius: 20px;
}
.onoffswitch-inner {
    display: block; width: 200%; margin-left: -100%;
    transition: margin 0.3s ease-in 0s;
}
.onoffswitch-inner:before, .onoffswitch-inner:after {
    display: block; float: left; width: 50%; height: 24px; padding: 0; line-height: 24px;
    font-size: 14px; color: white; font-family: Trebuchet, Arial, sans-serif; font-weight: bold;
    box-sizing: border-box;
}
.onoffswitch-inner:before {
    content: "ON";
    padding-left: 10px;
    background-color: #473e3c; color: #FFFFFF;
}
.onoffswitch-inner:after {
    content: "OFF";
    padding-right: 10px;
    background-color: #EEEEEE; color: #999999;
    text-align: right;
}
.onoffswitch-switch {
  height: 15px;
  display: block; width: 14px; margin: 5px;
  background: #FFFFFF;
  position: absolute; top: 2px; bottom: 0;
  right: 55px;
  border: 2px solid #999999; border-radius: 20px;
  transition: all 0.3s ease-in 0s;
}
.onoffswitch-checkbox:checked + .onoffswitch-label .onoffswitch-inner {
    margin-left: 0;
}
.onoffswitch-checkbox:checked + .onoffswitch-label .onoffswitch-switch {
    right: 0px;
}

.go-button button {
  background-color: #473e3c;
  color: white;
}
</style>
