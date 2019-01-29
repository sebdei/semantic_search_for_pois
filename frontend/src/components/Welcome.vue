<template>
  <div>
    <div class="header pt-5">
      <h2 class="header-text text-center">
        Choose your option
      </h2>
    </div>
    <div class="main">
      <transition name="twitter">
        <div v-show="activeTwitter" @click="pickInput('twitter')" class="twitter-input b-card clearfix">
          <TwitterInput :active="this.choosedInput==='twitter' ? true : false" @deactivate="deactivate">
          </TwitterInput >
        </div>
      </transition>

      <transition name="text">
        <div v-show="activeText" @click="pickInput('text')" class="text-input b-card clearfix">
          <TextInput :active="this.choosedInput==='text' ? true : false" @deactivate="deactivate">
          </TextInput>
        </div>
      </transition>
    </div>
    <div class="footer">
      <div class="presented">
        <div >
          <a href="https://www.uni-muenster.de/de/">
            <img src="https://upload.wikimedia.org/wikipedia/commons/7/7f/Logo_WWU_M%C3%BCnster.svg" />
          </a>
        </div>
        <div >
          <a href="https://www.wi.uni-muenster.de/department/dbis">
            <img src="http://www.ercis-launchpad.de/images/logo_dbis.png" />
          </a>
        </div>
      </div>

      <div class="thanks-source">
        <a href="https://daten.berlin.de/">
          <img id="open-berlin-img" src="https://www.berlin.de/css/berlin_de/echo/images/logo_berlin_de.svg">
        </a>
        <a href="https://www.visitberlin.de/de">
          <img class="open-berlin-img" src="https://pictures.attention-ngn.com/portal/24/256207/logo/1359725519.9371_3_o.jpg">
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
</template>

<script>
import TextInput from '@/components/TextInput'
import TwitterInput from '@/components/TwitterInput'

export default {
  components: {
    TextInput,
    TwitterInput
  },
  data () {
    return {
      choosedInput: ''
    }
  },
  computed: {
    activeText: function () {
      return !this.choosedInput || this.choosedInput==='text'
    },
    activeTwitter: function () {
      return !this.choosedInput || this.choosedInput==='twitter'
    }
  },
  methods: {
    pickInput: function (option) {
      this.choosedInput = option
    },
    deactivate: function () {
      this.$nextTick(()=> {
        this.choosedInput = ''
      })
    }
  }

}
</script>

<style scoped>
.header {
  height: 150px;
  background-color: #463E3C;
  color: white;
}
.main {
  width: 100%;
  overflow: hidden;
  display: flex;
}

.b-card {
  position: relative;
  height: 360px;
  cursor: pointer;
  flex-direction: row;
  width: 100%;
}

.text-enter-active, .text-leave-active,
.twitter-enter-active, .twitter-leave-active {
  transition: all .5s;
}
.text-enter-to {
  width: 100%;
}
.text-enter, .text-leave-to {
  width: 0%;
}

.twitter-enter, .twitter-leave-to {
  width: 0%;
}

.twitter-enter-to {
  width: 100%;
}

.footer {
  padding: 40px;
}

.presented {
  display: flex;
  justify-content: space-between;
  margin-bottom: 30px;
}

.presented img {
  width: 150px;
  margin: 0
}

.thanks-source {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.thanks-source img {
  margin: 0 5px;
  width: 60px;
}

#open-berlin-img {
  width: 70px;
}

</style>
