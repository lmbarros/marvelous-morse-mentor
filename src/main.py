def main():
    import hardware
    import state_manager
    import welcome_state

    hw = hardware.Hardware()
    sm = state_manager.StateManager(hw, welcome_state.WelcomeState())

    while True:
        hw.process_input(sm)
        sm.tick()


if __name__ == '__main__':
    main()
