<template>
    <div id="app">
        <div v-for="p in plots" :key="p.name" :id="p.name"></div>
    </div>
</template>

<script>

export default {
    name: 'app',
    data() {
        return {
            plots: [],
        };
    },
    created() {
        const context = require.context('./plots', true, /\.json$/);
        const plots = [];
        context.keys().forEach((key) => {
            plots.push(Object.assign({
                name: key.replace(/(^.*\/)|(\.json$)/g, ''),
            },
            context(key)));
        });
        this.plots = plots;
    },
    mounted() {
        console.log(JSON.stringify(this.plots));
        this.plots.forEach(p => {
            Plotly.plot(p.name, p.data, Object.assign({
                // width: 1600,
                // height: 600,
                legend: {
                    orientation: "h",
                }
            }, p.layout, { modeBarButtonsToRemove: ['sendDataToCloud'] }))
            .then((gd) => {
                Plotly.toImage(gd, { height: 450, width: 800 })
                .then((url) => {
                    p.img_data = url;
                    console.log('Generated image for', p.name);
                });
            });
        });
    },
}
</script>

<style>
#app {
    font-family: 'Avenir', Helvetica, Arial, sans-serif;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-align: center;
    color: #2c3e50;

}
div {
    display: inline-block;
}
</style>
