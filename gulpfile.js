const gulp = require('gulp');
const concat = require('gulp-concat');
const uglify = require('gulp-uglify');
const sourcemaps = require('gulp-sourcemaps');
const less = require('gulp-less');

const paths = {
  scripts_src:  'cards/static/**/*.js',
  scripts_dest: './cards/static/',
  styles_src: 'cards/static/**/*.less',
  destination: './cards/static/',
};


gulp.task('scripts', function() {
  return gulp.src(paths.scripts_src)
    .pipe(sourcemaps.init())
      .pipe(uglify())
      .pipe(concat('cards.min.js'))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(paths.destination));
});

gulp.task('styles', function() {
  return gulp.src(paths.styles_src)
    .pipe(sourcemaps.init())
      .pipe(less())
      .pipe(concat('cards.min.css'))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(paths.destination));
});

gulp.task('default', ['scripts', 'styles']);

