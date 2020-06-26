<template>
  <div style="position:relative" v-bind:class="{'open':openSuggestion}">
    <b-form-input
      type="text"
      v-model="selection"
      @keydown.enter="enter"
      @keydown.down="down"
      @keydown.up="up"
      @input="change"
    />
    <!-- <ul class="autocomplete-suggestions">
      <li
        v-for="(suggestion, $index) in matches" v-bind:key="$index"
       v-bind:class="{'active': isActive($index)}"
        @click="suggestionClick($index)"
      >
        <p href="#">{{ suggestion }}</p>
      </li>
    </ul> -->
    <vue-bootstrap-typeahead 
  v-model="query"
  :data="this.annotations"
/>
  </div>
</template>

<script>
import annotations_json from '../assets/ecoli_go_annotations.json'
export default {
  data() {
    return {
      open: false,
      current: 0,
      annotations: []
    };
  },
  created() {
      this.annotations = annotations_json
  },
  props: {
    suggestions: {
      type: Array,
      required: true
    },
    selection: {
      type: String,
      required: true,
      twoWay: true
    }
  },
  computed: {
    matches() {
      return this.suggestions.filter(str => {
        return str.indexOf(this.selection) >= 0;
      });
    },
    openSuggestion() {
      return (
        this.selection !== "" && this.matches.length != 0 && this.open === true
      );
    }
  },
  methods: {
    enter() {
      this.selection = this.matches[this.current];
      this.open = false;
    },
    up() {
      if (this.current > 0) this.current--;
    },
    down() {
      if (this.current < this.matches.length - 1) this.current++;
    },
    isActive(index) {
      return index === this.current;
    },
    change() {
      if (this.open == false) {
        this.open = true;
        this.current = 0;
      }
    },
    suggestionClick(index) {
      this.selection = this.matches[index];
      this.open = false;
    }
  }
};
</script>

<style scoped>
.autocomplete-suggestions {
    list-style: none;
    position: absolute;
    padding: 0;
    border-bottom-left-radius: 1rem;
    border-bottom-right-radius: 1rem;
    box-shadow: 1px 10px 15px #00000024;
    z-index: 100;
    background-color: white;
}
li {
padding: .1rem 1rem .1rem 1rem;
}
li:hover {
    background-color: #e9ecef;
}
p {
    margin-bottom: 0 !important;
    color: #6c757d;
}
</style>