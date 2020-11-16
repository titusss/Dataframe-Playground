<template>
    <div class="wrapper">
        <div class="sub_wrapper">
            <img :src="require(`@/assets/add_plugin_filled_shadow.svg`)" alt="">
        </div>
    </div>
</template>

<style scoped>
img {
    width: 64px;
}
.wrapper {
    display: flex;
    align-items: center;
    height: 100%;
    background-image: linear-gradient(60deg, #29323c 0%, #485563 100%);
    box-shadow: 4px 10px 20px rgba(0, 0, 0, 0.05);
    border-radius: 1rem;
    padding: 1.3rem;
    transition: transform 250ms ease, box-shadow 250ms ease;
    border-radius: 1rem;
    cursor: pointer;
}
.wrapper:hover {
  transform: translate(0px, -5px);
  box-shadow: 5px 30px 40px rgba(0, 0, 0, 0.15);
}
</style>