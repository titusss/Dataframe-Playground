<template>
  <iframe id="iframe_visualization" v-bind:src="vis_link" frameborder="0"></iframe>
</template>

<script>

export default {
    name: "visualization",
    props: {
        vis_link: String
    },
}
</script>

<style>
#iframe_visualization {
    width: 90vw;
    height: 80vh;
}
</style>