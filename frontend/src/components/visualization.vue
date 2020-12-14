<template>
  <div>
    <iframe id="iframe_visualization" v-bind:src="vis_link" frameborder="0"></iframe>
  </div>
</template>

<script>
export default {
  name: "visualization",
  props: {
    vis_link: String
  },
  created() {
    this.vis_link
    // this.vis_link = this.$route.query.vis
    console.log(this.vis_link);
  },
};
</script>

<style>
#iframe_visualization {
  width: 100%;
  height: 110vh;
  border-radius: 20px;
  padding: 10px;
  background-color: #fff;
}
</style>