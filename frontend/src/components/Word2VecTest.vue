<template>
  <div style="width: 500px; margin-left: 200px;">
    <form @submit.prevent="submitQuery">
      <div class="form-group">
        <textarea class="form-control" v-model="query" placeholder="Enter any query" />
        <button class="btn btn-primary">submit</button>
      </div>
    </form>

    <div v-for="(result, index) in results" class="my-5" :key="index">
      {{ index + 1 }}: {{ result.name }}, {{ result.similarity }} 
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data () {
    return {
      query: '',
      results: []
    }
  },
  methods: {
    submitQuery: async function () {
      let host = window.location.hostname;
      let response = await axios.post(`http://${host}:5000/classify`, {query: this.query})
      this.results = response.data
    }
  }
}
</script>
