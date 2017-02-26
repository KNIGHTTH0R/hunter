'use strict';
var gulp = require('gulp');
var concat = require('gulp-concat');
var uglify = require('gulp-uglify');
var js_obfuscator = require('gulp-js-obfuscator');

gulp.task('default', function() {
  gulp.src(['./app/js/*'])
    .pipe(concat('all.js'))
    .pipe(uglify({mangle:true}))
    .pipe(js_obfuscator({}, ["*.js"]))
    .pipe(gulp.dest('./dist/'))
});