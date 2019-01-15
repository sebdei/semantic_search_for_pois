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
  height: 300px;
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
</style>
