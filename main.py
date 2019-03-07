from naadi import collector, data_acquisitor, analyzer, presenter, web_gui


def main():
    module_netflow_collector = collector.main()
    module_data_acquisitor = data_acquisitor.main()
    module_presenter = presenter.main()
    module_analyzer = analyzer.main(module_presenter)
    module_gui = web_gui.main(module_netflow_collector, module_data_acquisitor, module_analyzer, module_presenter)


if __name__ == '__main__':
    main()
