<template>
    <div class="plugin_card" @click="emit_plugin_clicked()" >
        <img :src="require(`@/assets/${img}`)" alt="">
        <div class="">
            <h5>{{title}}</h5>
            <p>{{desc}}</p>
        </div>
    </div>
</template>

<script>
export default {
  name: "plugins",
  props: {
    title: String,
    desc: String,
    img: String
  },
  methods: {
      emit_plugin_clicked() {
          this.$emit('plugin_clicked');
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
    color: #9A9A9A;
    font-size: 0.75rem;
    margin-bottom: 0 !important;
}
h4 {
    margin: 0;
}
.plugin_card {
    display: grid;
    align-items: center;
    grid-template-columns: repeat(2, 1fr);
    grid-template-rows: repeat(1, 1fr);
    padding: 1.3rem;
    border-radius: 1rem;
    text-align: left;
    background-color: #f8f9fa;
    transition: transform 250ms ease, box-shadow 250ms ease;
    cursor: pointer;
    box-shadow: 4px 10px 20px rgba(0, 0, 0, 0.05);
}
.plugin_card:hover {
    box-shadow: 5px 30px 40px rgba(0, 0, 0, 0.1);
    transform: translate(0px, -5px);
}
</style>