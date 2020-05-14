<template>
<div>
<p>{{this.$route.query.config}}</p>
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
        // this.vis_link = this.$route.query.vis
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