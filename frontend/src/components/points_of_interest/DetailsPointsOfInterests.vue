<template>
  <div class="detail-side" >
    <div class="header pt-5">
      <h2 class="header-text text-center">
        Your personal recommendation
      </h2>
    </div>

    <div v-if="recommendation" class="poi-item">
      <div class="back-button mb-3" @click="backToList">
        <i class="fas fa-chevron-left fa-2x"></i>
      </div>
      <h5 class="font-weight-bold">
        {{ recommendation.name }}
      </h5>
      <div class="city">
        {{ this.city }}
      </div>
      <div class="teaser-text-wrapper">
        <div class="teaser-text">
          <p v-if="recommendation.source.text">
            {{  recommendation.source.text }}
          </p>
        </div>
        <div class="mb-2">
          <a
            v-if="recommendation.source.url"
            :href="recommendation.source.url">
              read more on {{ recommendation.source.url.includes('visitberlin') ? 'VisitBerlin' : 'Wikipedia' }}
          </a>
        </div>
      </div>
      <div class="bottom-wrapper">
        <div class="street font-weight-bold mb-3" @click.prevent="navigateTo(recommendation.lat, recommendation.long)">
          <div class="distance-box">
            <i class="fas fa-map-marker-alt orange mr-2"></i>
            <span v-if="this.distance">
              {{ this.distance }} km
            </span>
          </div>
          <div v-if="recommendation.street_name">
            <i class="fas fa-home orange mr-2"></i>
              {{ recommendation.street_name }} {{ recommendation.street_number }}
          </div>
        </div>
        <div class="like-wrapper">
          <div :class="[recommendation.liked === true ? 'orange' : '']" @click="likePoi($route.params.id)"><i class="far fa-thumbs-up fa-2x"></i></div>
          <div :class="[recommendation.liked === false ? 'orange' : '']" @click="dislikePoi($route.params.id)"><i class="far fa-thumbs-down fa-2x"></i></div>
        </div>
      </div>
      <div class="thanks float-right">
        <div class="thanks-text mr-2">
          thanks to
        </div>
        <div class="thanks-source">
          <a href="https://daten.berlin.de/">
            <img class="open-berlin-img" src="https://www.berlin.de/css/berlin_de/echo/images/logo_berlin_de.svg">
          </a>
          <a href="https://www.openstreetmap.org">
            <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/b/b0/Openstreetmap_logo.svg/1200px-Openstreetmap_logo.svg.png">
          </a>
          <a href="https://wikipedia.org">
            <img src="https://upload.wikimedia.org/wikipedia/en/thumb/8/80/Wikipedia-logo-v2.svg/1920px-Wikipedia-logo-v2.svg.png">
          </a>
        </div>
      </div>
    </div>

    <l-map v-if="recommendation" ref="myMap" class="map" :zoom="initZoom" :center="berlinMainTrainstationLeaflet">
      <l-tile-layer :url="layerUrl" :attribution="attribution"></l-tile-layer>
      <l-marker :lat-lng="berlinMainTrainstationLeaflet" ></l-marker>
      <l-marker v-for="(poimarker, index) in poiMarkers" :lat-lng="poimarker.geoLocation" :icon="poimarker.icon" :key="index"></l-marker>
    </l-map>
  </div>
</template>

<script>
import axios from 'axios'

import { LMap, LTileLayer, LMarker, L } from 'vue2-leaflet';
import { calcDistance, navigateTo } from '@/service/osm-service'
import { getCookie } from '@/service/cookie-service'

export default {
  components: {
    LMap,
    LTileLayer,
    LMarker
  },
  data () {
    return {
      attribution:'&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
      berlinMainTrainstationLeaflet: L.latLng(52.525084, 13.369402), // for demo purpose: use berlin station as start point
      city: 'Berlin',
      distance: null,
      initZoom: 11,
      liked: '',
      layerUrl:'http://{s}.tile.osm.org/{z}/{x}/{y}.png',
      recommendation: null,
      poiMarkers: []
    }
  },
  mounted () {
    this.fetchRecommendation()
  },
  methods: {
    backToList: function () {
      this.$router.push({ name: `list`, params: { disableSearchOptionsProp: true } })
    },
    fetchRecommendation: async function () {
      let host = window.location.hostname
      let userId = getCookie('user_id')
      let response = await axios.get(`http://${host}:5000/points_of_interests/${this.$route.params.id}/${userId ? userId : ''}`)

      const recommendation = response.data[0]
      this.setLocationVariables(recommendation)

      this.recommendation = recommendation
    },
    dislikePoi: async function (poiId) {
      this.recommendation.liked = false
      let postBody = {
        rating: false,
        poi_id: poiId
      }

      let userId = getCookie('user_id')
      let host = window.location.hostname
      await axios.post(`http://${host}:5000/users/${userId}/rate_poi`, postBody)
    },
    likePoi: async function (poiId) {
      this.recommendation.liked = true
      let postBody = {
        rating: true,
        poi_id: poiId
      }

      let userId = getCookie('user_id')
      let host = window.location.hostname
      await axios.post(`http://${host}:5000/users/${userId}/rate_poi`, postBody)
    },
    pushMarker: function (lat, long) {
      let icon = L.icon({
        iconUrl: './map-marker-2-xxl.png',
        iconSize: [33, 35]
      })

      let newMarker = { geoLocation: { lat: lat, lng: long }, icon: icon }
      this.poiMarkers.push(newMarker)
    },
    setLocationVariables: function (recommendation) {
      if (recommendation.lat && recommendation.long) {
        this.distance = calcDistance(this.berlinMainTrainstationLeaflet, recommendation.lat, recommendation.long)
        this.pushMarker(recommendation.lat, recommendation.long)
      }
    },
    navigateTo: navigateTo
  }
}
</script>

<style scoped>
.header {
  height: 150px;
  background-color: #463E3C;
  color: white;
}

.poi-item {
  min-height: 280px;
  padding: 30px 30px;
  border-top: 1px solid;
}

.street {
  flex-grow: 1;
  cursor: pointer;
}

.distance-box {
  display: inline-block;
  padding: 5px;
}

.teaser-text-wrapper {
  display: inline-block;
}

.teaser-text {
  display: -webkit-box;
  height: 100px;
  line-height: 1.2;
  -webkit-line-clamp: 5;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.teaser-text p {
  font-family: "Droid Serif";
  font-size: 14px;
  font-style: normal;
  font-variant: normal;
  font-weight: 400;
  line-height: 20px;
  text-align: justify;
}

.bottom-wrapper {
  display: flex;
  flex-direction: row;
  margin-bottom: 20px;
}

.like-wrapper {
  flex-grow: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.like-wrapper div {
  margin: 0 10px;
}

.thanks-text {
  display: inline;
  font-family: "Droid Serif";
  font-size: 0.9em;
}

.thanks-source {
  display: inline-block;
}

.thanks-source img {
  margin: 0 5px;
  width: 40px;
}

.map {
  width: 100%;
  height: 400px;
}

.orange {
  color: #e44802
}

.open-berlin-img {
  width: 60px!important;
}
</style>
