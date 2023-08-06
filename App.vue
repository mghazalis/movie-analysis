<template>
  <div>
    <TopMovies :topMovies="top10Movies" />
    <GenreMarketShare :genreMarketShare="genreMarketShareData" />
    <!-- Other components or content -->
  </div>
</template>

<script>
import axios from 'axios';
import Papa from 'papaparse';
import TopMovies from './components/TopMovies.vue';
import GenreMarketShare from './components/GenreMarketShare.vue';

export default {
  components: {
    TopMovies,
    GenreMarketShare,
  },
  data() {
    return {
      top10Movies: [],
      genreMarketShareData: {},
    };
  },
  mounted() {
    // Fetch and process data here
    axios.get('/data/movie.csv').then((response) => {
      const moviesData = Papa.parse(response.data, { header: true }).data;
      // Process the data to extract the top 10 movies
      this.top10Movies = moviesData.sort((a, b) => b.rating - a.rating).slice(0, 10);
    });

    axios.get('/data/rating.csv').then((response) => {
      const ratingsData = Papa.parse(response.data, { header: true }).data;
      // Process the data to calculate the market share of movie genres
      const genreMarketShare = {};
      for (const rating of ratingsData) {
        const movieId = rating.movieId;
        const genres = this.getMovieGenres(movieId);
        if (genres && genres.length > 0) {
          for (const genre of genres) {
            if (!genreMarketShare[genre]) {
              genreMarketShare[genre] = 0;
            }
            genreMarketShare[genre] += 1;
          }
        }
      }
      // Calculate the total number of ratings to calculate market share
      const totalRatings = ratingsData.length;
      for (const genre in genreMarketShare) {
        genreMarketShare[genre] = (genreMarketShare[genre] / totalRatings) * 100;
      }
      this.genreMarketShareData = genreMarketShare;
    });
  },
  methods: {
    getMovieGenres(movieId) {
      const movie = this.top10Movies.find((m) => m.movieId === movieId);
      return movie ? movie.genres.split('|') : [];
    },
  },
};
</script>
