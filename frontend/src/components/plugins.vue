<template>
  <div class="wrapper">
    <div
      class="plugin_card plugin_selected"
      v-bind:class="{plugin_selected_expanded:this.isSelected}"
      @click="plugin_selected()"
    >
      <img :src="this.image_url" alt />
      <div class>
        <h5>{{title}}</h5>
        <p>{{desc}}</p>
      </div>
    </div>
    <div class="plugin_card card_shadow" @click="plugin_selected()">
      <img :src="this.image_url" alt />
      <div class>
        <h5>{{title}}</h5>
        <p>{{desc}}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "plugins",
  props: {
    title: String,
    desc: String,
    image_url: String,
    active_plugin: String,
    id: String
  },
  data() {
    return {
      isSelected: false
    };
  },
  watch: {
    active_plugin: {
      handler() {
        this.toggle_selected();
      }
    }
  },
  methods: {
    plugin_selected() {
      this.$emit("plugin_selected")
    },
    toggle_selected() {
      if (this.id == this.active_plugin) {
        this.isSelected = true;
      } else {
        this.isSelected = false;
      }
    }
  },
  created() {
    if (this.id == this.active_plugin) {
      this.$emit("plugin_selected")
    }
    this.toggle_selected();
  }
};
</script>

<style scoped>
img {
  width: 64px;
  height: 64px;
  margin-right: 1rem;
  grid-area: 1 / 1 / 3 / 2;
}
p {
  color: #9a9a9a;
  font-size: 0.75rem;
  margin-bottom: 0 !important;
}
h4 {
  margin: 0;
}
.wrapper {
  position: relative;
  transition: transform 250ms ease, box-shadow 250ms ease;
  box-shadow: 4px 10px 20px rgba(0, 0, 0, 0.05);
  border-radius: 1rem;
}
.wrapper:hover {
  transform: translate(0px, -5px);
  box-shadow: 5px 30px 40px rgba(0, 0, 0, 0.15);
}
.plugin_card {
  height: 100%;
  display: grid;
  align-items: center;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(1, 1fr);
  padding: 1.3rem;
  border-radius: 1rem;
  text-align: left;
  background-color: #f8f9fa;
  transition: box-shadow 250ms ease;
  cursor: pointer;
}

.plugin_selected > img {
  filter: brightness(2.5) saturate(0);
}
.plugin_selected {
  /* background-color: #007bff; */
  /* background-image: linear-gradient(to right, #6a11cb 0%, #2575fc 100%); */
  /* background-image: linear-gradient(to top, #09203f 0%, #537895 100%); */

  background-image: linear-gradient(60deg, #29323c 0%, #485563 100%);
  /* background-image: linear-gradient(-225deg, #FF057C 0%, #7C64D5 48%, #4CC3FF 100%); */
  /* background-image: linear-gradient(-225deg, #A445B2 0%, #D41872 52%, #FF0066 100%); */
  /* background-image: linear-gradient(-45deg, #09203f 0%, #537895 100%); */

  /* background-image: linear-gradient(to right, #868f96 0%, #596164 100%); */
  /* background-image: linear-gradient(to top, #1e3c72 0%, #1e3c72 1%, #2a5298 100%); */
  /* background-image: linear-gradient(-225deg, #22E1FF 0%, #1D8FE1 48%, #625EB1 100%); */
  color: #fff;
  position: absolute;
  width: 100%;
  z-index: 10;
  clip-path: circle(0% at 110% 110%);
  opacity: 0;
  transition: clip-path 200ms ease-out, opacity 250ms ease-in;
}
.plugin_selected > div > p {
  color: #fff;
}
.plugin_selected_expanded {
  opacity: 1;
  clip-path: circle(170% at 110% 110%);
}
</style>
