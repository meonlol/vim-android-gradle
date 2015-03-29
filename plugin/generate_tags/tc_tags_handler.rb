require "minitest/autorun"

require_relative "tags_handler"
require_relative "../mock_kernel"

class TestTagsHandler < Minitest::Test

	def setup()
		Kernel.reinit()
		@testTools = TestTools.new()
		@tagsHandler = TagsHandler.new()

		@android_home_value = "stub/android/home"
		ENV['ANDROID_HOME'] = @android_home_value
	end

	def teardown()
		@testTools.removeTestFilesAndDirs()
	end



	def test_generateTagsFile_shouldCallShell()
		@testTools.createTestBuildFile()

		# Since we have to make sure the the child process in the fork finishes
		# first, we wait a 1/4th of a second here
		#sleep(1.0/4) TODO Doesn't work

		assert Kernel.getSystem.size > 2, "Kernel shell should have been called"
	end

	def test_isAlreadyRunning_shouldReturnFalseWhenIsNotRunning()
		resultNotRunning = @tagsHandler.isAlreadyRunning()

		@testTools.createTestFile(".tempTags")
		resultRunning = @tagsHandler.isAlreadyRunning()

		assert(resultRunning, "Should be running")
		assert(resultNotRunning == false, "Should not be running")
	end

	def test_getCtagsCommand_shouldGenerateCommandArray()
		@testTools.createTestBuildFile()

		result = @tagsHandler.getCtagsCommand()

		expectedCommand = ['ctags','--recurse','--fields=+l','--langdef=XML','--langmap=Java:.java,XML:.xml','--languages=Java,XML','--regex-XML=/id="([a-zA-Z0-9_]+)"/\\1/d,definition/']
        expectedCommand += ['-f', '.tempTags']
		expectedCommand += PathResolver.new.getAllSourcePaths()

		assert_equal(expectedCommand, result, "Should have generated the right command")
	end

	def test_executeCommandAsyncly_shouldCallKernelWithArray()
		command = ['a', 'b', 'c']
		@testTools.createTestFile(".tags")
		@testTools.createTestFile(".tempTags")

		@tagsHandler.executeShellCommand(command)

		assert_equal command, Kernel.getSystem, "Should have called command on Kernel"
		assert File.exists?(".tempTags") == false, ".tempTags should have been removed"
		assert File.exists?(".tags") == true, ".tags should have been replaced with .tempTags"
	end

end
