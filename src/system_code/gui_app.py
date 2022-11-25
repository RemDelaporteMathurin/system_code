import system_code as tsc
import streamlit as st


def main():
    
    st.header(
        """
        System code
        """
    )
    
    selected_example = st.selectbox(
        label='Select and example',
        options=[
            "balanced_scenario",
            "icf_example",
            "over_produce_scenario",
            "under_produce_scenario",
        ]
    )
    
    if selected_example == "icf_example":
        # TODO add flow diagram image
        # st.image("url to image")
        col1, col2, col3 = st.columns(3)

        col1.header("Plasma")
        plasma_volume = col1.number_input('Plasma volume', value=1., min_value=0.)
        plasma_burning_rate = col1.number_input('Plasma burning rate', value=1., min_value=0.)
        plasma_initial_concentration = col1.number_input('Plasma initial concentration', value=0., min_value=0.)

        col2.header("Breeder")
        breeder_volume = col2.number_input('breeder volume', value=1., min_value=0.)
        breeder_generation_term = col2.number_input('breeder burning rate', value=1.05, min_value=0.)
        breeder_initial_concentration = col2.number_input('breeder initial concentration', value=0., min_value=0.)

        col3.header("Storage")
        storage_volume = col3.number_input('storage volume', value=1., min_value=0.)
        storage_fueling_rate = col3.number_input('storage fueling rate', value=1., min_value=0.)
        storage_initial_concentration = col3.number_input('storage initial concentration', value=5., min_value=0.)
        
        
        plasma = tsc.Plasma(
            name="Plasma",
            volume=plasma_volume,
            plasma_burning_rate=plasma_burning_rate,
            initial_concentration=plasma_initial_concentration
        )

        breeder = tsc.Box(
            name="Breeder",
            volume=breeder_volume,
            generation_term=breeder_generation_term,
            initial_concentration=breeder_initial_concentration
        )

        storage = tsc.StorageAndDeliverySystem(
            name="Storage",
            output=plasma,
            volume=storage_volume,
            fueling_rate=storage_fueling_rate,
            initial_concentration=storage_initial_concentration
        )
        
        plasma.add_output(storage, 1)
        breeder.add_output(storage, 1)
        
        my_system = tsc.System([storage, plasma, breeder])
        
        col1_section2, col2_section2, = st.columns([1,3])
        
        duration = col1_section2.number_input('Duration of run', value=20, min_value=0, step=1)
        run = col1_section2.button('Run')
        if run:
            my_system.run(duration)

            inventory_plt = my_system.plot_inventories()
            concentration_plt = my_system.plot_concentrations()
            
            st.pyplot(inventory_plt)
            st.pyplot(concentration_plt)


    else:
        st.write("Not implemented yet")

if __name__ == "__main__":
    main()
