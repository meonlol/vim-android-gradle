#! /usr/bin/env python

import re
import os
import sys

class PathsResolver:
    def __init__(self):
        sys.path.append(os.getcwd())


    def getAllClassPaths(self):
        classPathsAndJars = []
        # x addProjectClassPath > '.bin/classes'
        # x addGradleSDKJar > 'platforms/android-19/android.jar'
        # - addGradleClassPath >
            # - /build/bundles/debug/classes.jar   ??
            # - /libs/*.jar
        # - addPropertiesClassPath > paths specified in project.properties (only non gradle?)

        classPathsAndJars.extend(self.getProjectSourcePaths()) # Does syntastic need this?
        classPathsAndJars.extend(self.getGeneratedProjectClassPaths())
        classPathsAndJars.extend(self.getGradleClassPathsFromFile())
        classPathsAndJars.append(self.getAndroidSdkJar())
        return classPathsAndJars

    def getAllSourcePaths(self):
        # 'paths' sourcePaths
        #addProjectClassPath > None
        #addGradleSDKJar > 'sources/android-19/'
        #addGradleClassPath >
            # ./src (if available)
        #addPropertiesClassPath > paths specified in project.properties (only non gradle?)

        sourcePaths = []
        sourcePaths.extend(self.getProjectSourcePaths())
        sourcePaths.append(self.getAndroidSdkSourcePath())
        return sourcePaths


    def getProjectSourcePaths(self):
        projectClassPath = './src/main/java'
        projectResPath = './src/main/res'
        #return ':'.join([projectClassPath, generatedSources])
        return [projectClassPath, projectResPath]

    def getGeneratedProjectClassPaths(self):
        generatedDebugClasses =  './build/intermediates/classes/debug'
        return [generatedDebugClasses]


    def getGradleClassPathsFromFile(self):
        list = []

        filename = 'gradle-sources'
        print os.getcwd()

        if (os.path.isfile(filename)):
            with open(filename, 'U') as f:
                for line in f:
                    list.append(line.rstrip())
        #return ':'.join(list)
        return list

    def getAndroidSdkJar(self):
        androidHome = os.environ.get('ANDROID_HOME')
        currentPlatformDir = 'android-' + self.getAndroidVersionFromBuildGradle()
        sdkJarPath = androidHome +os.sep+ 'platforms' +os.sep+ currentPlatformDir +os.sep+ 'android.jar'
        return sdkJarPath

    def getAndroidSdkSourcePath(self):
        androidHome = os.environ.get('ANDROID_HOME')
        currentPlatformDir = 'android-' + self.getAndroidVersionFromBuildGradle()
        sdkSourcePath = androidHome +os.sep+ 'sources' +os.sep+ currentPlatformDir +os.sep
        return sdkSourcePath


    def getAndroidVersionFromBuildGradle(self):
        with open('build.gradle', 'U') as f:
            for line in f:
                result = self.getAndroidVersionFromLine(line)
                if (result != None):
                    return result

    def getAndroidVersionFromLine(self, line):
        matchObj = re.search( r'compileSdkVersion\W*(\d*)', line, re.M|re.I)
        if matchObj != None:
            version = matchObj.group(1)
            return version
        return None
