from envisage.ui.tasks.api import TasksApplication

def main():
    app = TasksApplication()
    app.on_trait_change(lambda: app.exit(force=True), "application_initialized")
    app.run()

if __name__ == "__main__":
    main()
