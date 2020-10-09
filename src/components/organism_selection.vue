<template>
  <div class="wrapper">
    <span class="dot" v-bind:class="{check_activated:this.organism.id == this.local_active_organism_id}">
      <b-icon class="check-icon" icon="check"></b-icon>
    </span>
    <div
      class="organism_card organism_selected"
      v-bind:class="{organism_selected_expanded:this.organism.id == this.local_active_organism_id}"
    >
      <img :src="this.image_url" alt />
      <div class>
        <h5>{{organism.name}}</h5>
        <p>{{organism.description}}</p>
      </div>
    </div>
    <div class="organism_card card_shadow">
      <img :src="this.image_url" alt />
      <div class>
        <h5>{{organism.name}}</h5>
        <p>{{organism.description}}</p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "organism_selection",
  props: {
    organism: Object,
    local_active_organism_id: String
  },
  created() {
    try { // This try catch try catch block allows for svg, png, and jpeg organism icons.
      this.image_url = require(`../assets/organisms${this.organism.path}/icon.svg`);
    } catch(e) {
      try {
        this.image_url = require(`../assets/organisms${this.organism.path}/icon.png`);
      } catch(f) {
        this.image_url = require(`../assets/organisms${this.organism.path}/icon.jpg`);
      }
    }
  },
  data() {
    return {
      is_selected: false,
      image_url: undefined,
    }
  }
}
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
.dot {
  z-index: 100;
  position: absolute;
  top: 0;
  right: 0;
  height: 24px;
  width: 24px;
  background-color: #007bff;
  /* border: 3px solid #007bff; */
  box-shadow: 1px 3px 8px #21252942;
  border-radius: 50%;
  display: inline-block;
  transform: translate(40%, -35%) scale(0.01);
  transition: transform 350ms cubic-bezier(.34,.35,.17,1.5);
}
.check-icon {
  fill: #fff;
  width: 18px;
  height: 18px;
  margin: 3px;
}
.check_activated {
  background-color: #007bff;
}

.check_activated {
  transform: translate(40%, -35%) scale(1);
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
.organism_card {
  height: 100%;
  display: grid;
  align-items: center;
  grid-template-columns: repeat(2, 1fr);
  grid-template-rows: repeat(1, 1fr);
  color: #9a9a9a;
  padding: 1.3rem;
  border-radius: 1rem;
  text-align: left;
  background-color: #f8f9fa;
  transition: box-shadow 250ms ease;
  cursor: pointer;
}

.organism_selected {
  /* background-image: linear-gradient(60deg, #29323c 0%, #485563 100%); */
  box-shadow: 0 0 0 4px #007bff;
  color: #485563;
  position: absolute;
  width: 100%;
  z-index: 10;
  clip-path: circle(0% at 110% 110%);
  opacity: 0;
  transition: clip-path 300ms ease-out, opacity 350ms ease-in;
}
.organism_selected > div > p {
  color: #485563;
}
.organism_selected_expanded {
  opacity: 1;
  clip-path: circle(170% at 110% 110%);
}
</style>