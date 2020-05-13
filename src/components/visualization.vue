<template>
<div>
<p>{{this.$route.query.vis}}</p>
  <iframe id="iframe_visualization" v-bind:src="vis_link" frameborder="0"></iframe>
</div>
</template>

<script>
export default {
    name: "visualization",
    data() {
        return {
            vis_link: null,
        }
    },
    created() {
        this.vis_link = this.$route.query.vis
        console.log(this.vis_link)
    }
}
</script>

<style>
#iframe_visualization {
    width: 100%;
    height: 150vh;
    border-radius: 20px;
    padding: 10px;
    background-color: #fff;
    margin-top: 3em;
}
</style>