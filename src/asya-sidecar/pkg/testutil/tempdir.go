package testutil

import "os"

// TempDir creates a temporary directory in /tmp and returns a cleanup function.
func TempDir() (string, func(), error) {
	dir, err := os.MkdirTemp("/tmp", "asya-test-")
	if err != nil {
		return "", func() {}, err
	}

	cleanup := func() {
		_ = os.RemoveAll(dir)
	}

	return dir, cleanup, nil
}
