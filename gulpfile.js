var gulp = require('gulp');
var runSequence = require('run-sequence');
var gutil = require('gulp-util');
var plumber = require('gulp-plumber');
var del = require('del');
var gulpif = require('gulp-if');
var argv = require('yargs').argv;
var es = require('event-stream')

var stylus = require('gulp-stylus');
var jeet = require('jeet');
var autoprefixer = require('gulp-autoprefixer');
var minifyCss = require('gulp-minify-css');
var uglify = require('gulp-uglify');
var fontmin = require('gulp-fontmin');

var changed = require('gulp-changed');
var imagemin = require('gulp-imagemin');
var jpegoptim = require('imagemin-jpegoptim');
var pngquant = require('imagemin-pngquant');


// Errors
var onError = function(err) {
    gutil.log(gutil.colors.red('¡Oh, no! 😱'));
    gutil.beep();
    console.log(err);
}

// --------------------------
// VARIABLES
// --------------------------

// Routes
var source = 'website/src/';
var static = 'website/static/';

// gulp build --production
var production = !!argv.production;
// determine if we're doing a build
var build = argv._.length ? argv._[0] === 'build' : false;
// for production we require the clean method on every individual task
var clean = build ? ['clean'] : [];

// --------------------------
// CUSTOMS TASKS
// --------------------------

// Clean
gulp.task('clean', function() {
	return del([static]);
});

// Copy assets
gulp.task('assets', clean, function() {
	var assets = gulp.src(source + 'assets/**/*')
		.pipe(gulp.dest(static + 'assets/'));
});

// Process Stylus and compress CSS
gulp.task('css', clean, function() {
	return gulp.src(source + 'css/styles.styl')
		.pipe(plumber({
			errorHandler: onError
		}))
		.pipe(stylus({
			use: [
				jeet()
			]
		}))
		.pipe(gulp.dest(static + 'css/'));
});

gulp.task('prefix', function() {
	return gulp.src(static + 'css/*.css')
		.pipe(plumber({
			errorHandler: onError
		}))
		.pipe(autoprefixer({
			browsers: ['last 3 versions'],
			cascade: true
		}))
		.pipe(gulpif(production, minifyCss()))
});

// Minify JS
gulp.task('js', clean, function(){
	return gulp.src(source + 'js/**/*.js')
		.pipe(gulpif(production, uglify()))
		.pipe(gulp.dest(static + 'js/'));
});

// Optimize Images
gulp.task('compress-images', clean, function() {
  return gulp.src(source + 'img/**/*')
		.pipe(changed(static + 'img/'))
		.pipe(imagemin([
			imagemin.gifsicle(),
			imagemin.svgo(),
			jpegoptim({
				progressive: true,
				max: 80
			}),
			pngquant({
				quality: 80,
				verbose: true
			})
    ],
		{
			verbose: true
		}))
		.pipe(gulp.dest(static + 'img/'));
});

// Optimize Fonts
gulp.task('compress-fonts', function() {
  return gulp.src(source + 'fonts/**/*')
    .pipe(fontmin())
    .pipe(gulp.dest(static + 'fonts/'));
})


// --------------------------
// DEV/WATCH TASKS
// --------------------------

gulp.task('build-css', function() {
	runSequence('css', 'prefix')
})

// WATCH task
gulp.task('watch', function() {
	//Watch changes in styles, js, html and images
	gulp.watch(source + 'css/*.styl', ['build-css']);
	gulp.watch(source + 'js/**/*.js', ['js']);
	gulp.watch(source + 'img/**/*', ['compress-images']);
  gulp.watch(source + 'fonts/**/*', ['compress-fonts']);
	gutil.log(gutil.colors.bgGreen('Watching for changes...'));
});

// BUILD task
gulp.task('build', function() {
	runSequence('assets', 'build-css', 'js', 'compress-images', 'compress-fonts')
});

// DEFAULT task
gulp.task('default', function() {
	runSequence('assets', 'build-css', 'js', 'compress-images', 'compress-fonts', 'watch')
})

// --------------------------
// RUN DJANGO MANAGE.PY RUNSERVER
// --------------------------

//var spawn = require('child_process').spawn;

// gulp.task('default', function() {
// 	// gulp.start('serve:backend');
// });

// Start DJANGO server
// gulp.task('serve:backend', function () {
// 	var devServerPort = process.env.PORT || 8000;
// 	process.env.PYTHONUNBUFFERED = 1;
// 	process.env.PYTHONDONTWRITEBITECODE = 1;
// 	spawn('python', ['manage.py', 'runserver', '0.0.0.0:' + devServerPort], {
// 		stdio: 'inherit'
// 	});
// });
